# LoadSysCompany

## Visão Geral

A task `LoadSysCompany` extrai dados de empresas (core_company) do ServiceNow baseado nas referências encontradas nos incidents. Esta é uma task de lookup inteligente que carrega apenas as empresas que são realmente utilizadas, otimizando o volume de dados e garantindo relevância.

## Características

- **Tipo**: Task de Referência (lookup baseado em uso)
- **Modelo**: `SysCompany`
- **Filtro Principal**: IDs de company presentes em Incident
- **Estratégia de Carga**: UPSERT (preserva timestamps ETL)  
- **Método**: Individual API calls (fetch_single_record)

## Implementação

### Classe Principal

```python
class LoadSysCompany(MixinGetDataset, Pipeline):
    def __init__(self):
        super().__init__()
```

### Estratégia de Lookup Inteligente

```python
@property
def _companies(self) -> pl.DataFrame:
    fields = ",".join([
        f.name for f in SysCompany._meta.fields 
        if not f.name.startswith("etl_") and f.name != "etl_hash"
    ])

    # IDs únicos de companies presentes em Incident
    qs = (
        Incident.objects.exclude(company__isnull=True)
        .exclude(company="")
        .values_list("company", flat=True)
        .distinct()
    )
    ids = sorted({x for x in qs if x})

    if not ids:
        # retorna DF vazio com schema correto
        return pl.DataFrame(
            schema={f.name: pl.String for f in SysCompany._meta.fields}
        )

    all_results: List[Dict] = []
    # chamadas individuais à API para cada sys_id
    for sid in ids:
        rec = fetch_single_record(
            path="core_company",
            sys_id=sid,
            params={"sysparm_fields": fields},
        )
        if rec:
            all_results.append(rec)

    return pl.DataFrame(
        all_results,
        schema={f.name: pl.String for f in SysCompany._meta.fields},
    )
```

**Características Únicas**:
- **Lookup Baseado em Uso**: Só carrega companies referenciadas em incidents
- **API Individual**: Não usa paginação, faz uma chamada por company
- **Filtro Dinâmico**: IDs vêm do banco local, não query ServiceNow
- **Performance**: Otimizada para volume pequeno mas essencial

## Diferenças de Outras Tasks

| Aspecto | Tasks Normais | LoadSysCompany |
|---------|---------------|----------------|
| **Fonte de Filtro** | Query ServiceNow | Banco local (Incident) |
| **Método API** | Paginação (paginate) | Individual (fetch_single_record) |
| **Volume** | Alto (1000s) | Baixo (10-100) |
| **Path API** | Tabela principal | `core_company` |
| **Dependência** | Independente | Depende de Incident |

## Estrutura de Company

### Campos Principais

**Identificação**:
- `sys_id` (PK) - ID único da empresa
- `name` - Nome da empresa
- `u_name` - Nome customizado  

**Localização**:
- `city` - Cidade
- `state` - Estado/Província
- `country` - País
- `zip` - CEP/Código Postal

**Contatos**:
- `phone` - Telefone principal
- `fax` - Fax
- `email` - Email principal
- `website` - Website

**Estrutura Organizacional**:
- `parent` - Empresa pai (hierarquia)
- `primary` - Empresa primária (true/false)

**Configurações**:
- `customer` - É cliente (true/false)
- `vendor` - É fornecedor (true/false)
- `manufacturer` - É fabricante (true/false)

### Exemplo de Company

```json
{
  "sys_id": "company_123abc",
  "name": "Banco Bradesco S.A.",
  "u_name": "Bradesco",
  "city": "Osasco", 
  "state": "São Paulo",
  "country": "Brasil",
  "zip": "06029-900",
  "phone": "+5511999887766",
  "email": "contato@bradesco.com.br",
  "website": "www.bradesco.com.br",
  "parent": "holding_456def",
  "primary": "true",
  "customer": "true",
  "vendor": "false",
  "manufacturer": "false"
}
```

## Performance e Otimização

### Por que Individual API Calls?

```python
# ❌ Paginação normal seria ineficiente:
# - Query: "sys_idIN[id1,id2,id3,...,id50]" 
# - 50 IDs únicos = query complexa
# - Muitas companies não utilizadas seriam retornadas

# ✅ Individual calls são otimizadas para este caso:
# - 50 calls individuais = rápido para volume baixo  
# - Apenas dados necessários
# - Cache do ServiceNow pode ajudar
```

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **IDs Únicos** | 20-80 companies | Baseado em incidents ativos |
| **API Calls** | 20-80 calls | Uma por company |
| **Taxa Sucesso** | 90-98% | Algumas companies podem não existir |
| **Tempo Total** | 30-90 segundos | Depende da latência da API |
| **Volume Final** | 15-70 records | Apenas companies encontradas |

### Otimizações Implementadas

```python
def _chunked(seq: List[str], size: int = 100) -> List[List[str]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]

# Preparado para processamento em chunks se necessário
# Atualmente não usado, mas disponível para volumes maiores
```

## Estratégia UPSERT

### Vantagens para Dados de Referência

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    upsert_by_sys_id(dataset=self.dataset, model=SysCompany, log=self.log)
    return self.log
```

**Por que UPSERT é Ideal**:
- **Dados Estáveis**: Companies mudam pouco
- **Volume Baixo**: UPSERT overhead é mínimo  
- **Preservação**: Mantém timestamps ETL
- **Incremental**: Apenas novas ou modificadas

### Processo de Lookup + UPSERT

```python
# 1. Busca IDs únicos no banco local
incident_company_ids = Incident.objects.values_list('company', flat=True).distinct()

# 2. Filtra IDs válidos (não-nulos, não-vazios)  
valid_ids = [id for id in incident_company_ids if id]

# 3. Para cada ID, busca dados no ServiceNow
servicenow_companies = []
for company_id in valid_ids:
    company_data = fetch_single_record("core_company", company_id)
    if company_data:
        servicenow_companies.append(company_data)

# 4. UPSERT no banco local
upsert_by_sys_id(dataset=servicenow_companies, model=SysCompany)
```

## Relacionamentos e Uso

### Com Incidents

```python
# Incidents por empresa
def incidents_by_company():
    """Distribuição de incidents por empresa"""
    
    # Join entre Incident e SysCompany
    from django.db.models import Count
    
    company_stats = Incident.objects.values(
        'company'
    ).annotate(
        incident_count=Count('sys_id')
    ).order_by('-incident_count')
    
    # Enriquecer com dados da empresa
    result = []
    for stat in company_stats[:10]:  # Top 10
        company = SysCompany.objects.filter(sys_id=stat['company']).first()
        
        result.append({
            'company_id': stat['company'],
            'company_name': company.name if company else f"ID: {stat['company']}",
            'incident_count': stat['incident_count'],
            'has_company_data': company is not None
        })
    
    return result

# Exemplo de saída:
# [
#   {'company_name': 'Banco Bradesco S.A.', 'incident_count': 1250, 'has_company_data': True},
#   {'company_name': 'Vita Tecnologia', 'incident_count': 890, 'has_company_data': True},
#   {'company_name': 'ID: unknown_123', 'incident_count': 45, 'has_company_data': False}
# ]
```

### Hierarquia de Empresas

```python
def build_company_hierarchy():
    """Constrói hierarquia de empresas"""
    
    companies = SysCompany.objects.all()
    
    # Mapear parent-child relationships
    hierarchy = {}
    orphans = []
    
    for company in companies:
        if not company.parent:
            # Empresa raiz
            hierarchy[company.sys_id] = {
                'company': company,
                'children': []
            }
        else:
            # Empresa filha
            parent_entry = hierarchy.get(company.parent)
            if parent_entry:
                parent_entry['children'].append(company)
            else:
                # Parent não encontrado (órfã)
                orphans.append(company)
    
    return {
        'hierarchy': hierarchy,
        'orphan_companies': orphans,
        'total_companies': companies.count()
    }

def print_company_tree():
    """Imprime árvore hierárquica de empresas"""
    
    hierarchy = build_company_hierarchy()
    
    for root_id, data in hierarchy['hierarchy'].items():
        root_company = data['company']
        print(f"🏢 {root_company.name}")
        
        for child in data['children']:
            print(f"  └── {child.name}")
        
        if not data['children']:
            print(f"  └── (sem filiais)")
```

## Validação de Dados

### Detecção de Companies Órfãs

```python
def find_missing_companies():
    """Encontra companies referenciadas mas não carregadas"""
    
    # IDs de companies referenciadas em incidents
    referenced_ids = set(
        Incident.objects.exclude(company__isnull=True)
        .exclude(company="")
        .values_list("company", flat=True)
        .distinct()
    )
    
    # IDs de companies carregadas
    loaded_ids = set(
        SysCompany.objects.values_list("sys_id", flat=True)
    )
    
    # Companies referenciadas mas não encontradas
    missing_ids = referenced_ids - loaded_ids
    
    if missing_ids:
        # Detalhes dos incidents órfãos
        orphan_incidents = Incident.objects.filter(
            company__in=missing_ids
        ).values('company').annotate(
            incident_count=Count('sys_id')
        )
        
        missing_details = []
        for item in orphan_incidents:
            missing_details.append({
                'company_id': item['company'],
                'incident_count': item['incident_count'],
                'sample_incidents': list(
                    Incident.objects.filter(company=item['company'])
                    .values_list('number', flat=True)[:3]
                )
            })
        
        return {
            'missing_count': len(missing_ids),
            'missing_details': missing_details,
            'total_referenced': len(referenced_ids),
            'total_loaded': len(loaded_ids),
            'load_success_rate': round((len(loaded_ids) / len(referenced_ids)) * 100, 1)
        }
    
    return {
        'missing_count': 0,
        'total_referenced': len(referenced_ids),
        'total_loaded': len(loaded_ids),
        'load_success_rate': 100.0
    }
```

### Limpeza de Dados

```python
def cleanup_unused_companies():
    """Remove companies não mais referenciadas"""
    
    # IDs atualmente referenciadas
    current_refs = set(
        Incident.objects.exclude(company__isnull=True)
        .exclude(company="")
        .values_list("company", flat=True)
        .distinct()
    )
    
    # Companies no banco que não são mais referenciadas
    unused = SysCompany.objects.exclude(sys_id__in=current_refs)
    
    if unused.exists():
        unused_count = unused.count()
        unused_names = list(unused.values_list('name', flat=True)[:10])
        
        logger.info(f"Companies não utilizadas encontradas: {unused_count}")
        logger.info(f"Exemplos: {unused_names}")
        
        # Opcional: remover após confirmação
        # unused.delete()
        
        return {
            'unused_found': unused_count,
            'examples': unused_names,
            'action': 'logged_only'  # ou 'deleted'
        }
    
    return {'unused_found': 0, 'action': 'none_needed'}
```

## Monitoramento

### Métricas de Referência

```python
def company_reference_metrics():
    """Métricas de referência de empresas"""
    
    # Stats básicas
    total_companies = SysCompany.objects.count()
    total_incidents = Incident.objects.count()
    incidents_with_company = Incident.objects.exclude(
        company__isnull=True
    ).exclude(company="").count()
    
    # Top empresas por volume de incidents
    top_companies = Incident.objects.values('company').annotate(
        incident_count=Count('sys_id')
    ).order_by('-incident_count')[:5]
    
    # Enriquecer com nomes
    enriched_top = []
    for item in top_companies:
        company = SysCompany.objects.filter(sys_id=item['company']).first()
        enriched_top.append({
            'company_name': company.name if company else f"ID: {item['company'][:8]}...",
            'incident_count': item['incident_count'],
            'has_data': company is not None
        })
    
    # Companies por tipo
    customer_count = SysCompany.objects.filter(customer='true').count()
    vendor_count = SysCompany.objects.filter(vendor='true').count()
    
    return {
        'overview': {
            'total_companies_loaded': total_companies,
            'total_incidents': total_incidents,
            'incidents_with_company': incidents_with_company,
            'company_coverage': round(
                (incidents_with_company / total_incidents) * 100, 1
            ) if total_incidents else 0
        },
        'top_companies': enriched_top,
        'company_types': {
            'customers': customer_count,
            'vendors': vendor_count,
            'mixed': SysCompany.objects.filter(
                customer='true', vendor='true'
            ).count()
        }
    }
```

### Alertas de Integridade

```python
def company_integrity_alerts():
    """Alertas de integridade dos dados de empresa"""
    
    alerts = []
    
    # 1. Companies órfãs (referenciadas mas não carregadas)
    missing_analysis = find_missing_companies()
    if missing_analysis['missing_count'] > 0:
        alerts.append({
            'type': 'missing_companies',
            'severity': 'warning',
            'message': f"{missing_analysis['missing_count']} companies referenciadas mas não carregadas",
            'success_rate': missing_analysis['load_success_rate']
        })
    
    # 2. Baixa cobertura de companies em incidents
    total_incidents = Incident.objects.count()
    with_company = Incident.objects.exclude(company__isnull=True).exclude(company="").count()
    
    if total_incidents > 0:
        coverage = (with_company / total_incidents) * 100
        if coverage < 80:  # Menos de 80% dos incidents têm company
            alerts.append({
                'type': 'low_company_coverage',
                'severity': 'info',
                'message': f'Apenas {coverage:.1f}% dos incidents têm company definida'
            })
    
    # 3. Companies sem dados básicos
    incomplete_companies = SysCompany.objects.filter(
        Q(name__isnull=True) | Q(name='') | 
        Q(city__isnull=True) | Q(city='')
    ).count()
    
    if incomplete_companies > 0:
        alerts.append({
            'type': 'incomplete_company_data',
            'severity': 'info', 
            'message': f'{incomplete_companies} companies com dados incompletos'
        })
    
    return alerts
```

## Execução e Agendamento

### Frequência Recomendada

```python
# ✅ Ideal: Após LoadIncidentsOpened
# Garante que novas companies referenciadas sejam carregadas

# ⚠️ Aceitável: Diário
# Companies mudam pouco, mas novas referências podem aparecer

# ❌ Evitar: Múltiplas vezes por dia
# Overhead desnecessário para dados estáveis
```

### Pipeline Integrada

```python
def integrated_reference_data_pipeline():
    """Pipeline integrada de dados de referência"""
    
    pipeline_results = {}
    
    # 1. Carregar incidents primeiro (fonte das referências)
    logger.info("Carregando incidents...")
    # LoadIncidentsOpened executaria aqui
    
    # 2. Carregar companies baseado nas referências
    logger.info("Carregando companies referenciadas...")
    company_task = LoadSysCompany()
    company_result = company_task.run()
    pipeline_results['companies'] = company_result
    
    # 3. Carregar users (similar ao LoadSysCompany)
    logger.info("Carregando users referenciados...")
    # LoadSysUser executaria aqui
    
    # 4. Validar integridade das referências
    logger.info("Validando integridade referencial...")
    missing_companies = find_missing_companies()
    pipeline_results['validation'] = missing_companies
    
    return pipeline_results
```

Esta task é fundamental para manter dados de referência atualizados e garantir que análises de incidents tenham informações completas sobre as empresas envolvidas.