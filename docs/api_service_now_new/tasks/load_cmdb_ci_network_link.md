# LoadCmdbCiNetworkLink

## Visão Geral

A task `LoadCmdbCiNetworkLink` extrai itens de CMDB (Configuration Management Database) relacionados a links de rede do ServiceNow. Estes dados representam as conexões físicas e lógicas entre equipamentos de rede, fornecendo visibilidade da topologia de rede para análises de impacto e troubleshooting.

## Características

- **Tipo**: Task de Configurações (sem período)
- **Modelo**: `CmdbCiNetworkLink`
- **Filtro Principal**: Company (empresa)
- **Estratégia de Carga**: UPSERT (preserva timestamps ETL)
- **Frequência**: Dados de configuração, executados esporadicamente

## Implementação

### Classe Principal

```python
class LoadCmdbCiNetworkLink(MixinGetDataset, Pipeline):
    def __init__(self):
        super().__init__()
```

### Query ServiceNow

```python
# aplicar filtro por assignment_group (fila) similar aos loaders de incidents
query = ""
add_q = "company.nameLIKEbradesco"
if add_q:
    query = add_q

params = {"sysparm_fields": fields}
if query:
    params["sysparm_query"] = query

result_list = paginate(
    path="cmdb_ci_network_link",
    params=params,
    limit=10000,
    mode="offset",
    limit_param="sysparm_limit",
    offset_param="sysparm_offset",
    result_key="result",
)
```

**Filtros Aplicados**:
- `company.nameLIKEbradesco` - Links de rede da empresa Bradesco (dot-walk)

**Diferença das Tasks de Incidents**: 
- Não filtra por data, busca todos os links ativos
- Usa dot-walk para filtrar pela empresa associada
- Aplica `.unique(subset="sys_id")` para evitar duplicatas

## Estrutura de Network Links

### Campos Principais

**Identificação**:
- `sys_id` (PK) - ID único do link
- `name` - Nome do link de rede
- `u_name` - Nome customizado

**Configuração de Rede**:
- `ip_address` - Endereço IP do link
- `mac_address` - Endereço MAC
- `dns_domain` - Domínio DNS

**Relacionamentos**:
- `company` - Empresa proprietária (referência)
- `location` - Localização física
- `u_environment` - Ambiente (prod, dev, etc.)

**Conectividade**:
- `port` - Porta de conexão  
- `speed` - Velocidade do link
- `duplex` - Modo duplex (full/half)

**Status Operacional**:
- `operational_status` - Status operacional
- `install_status` - Status de instalação
- `u_status` - Status customizado

**Auditoria**:
- `sys_created_on`, `sys_created_by`
- `sys_updated_on`, `sys_updated_by`

### Exemplo de Network Link

```json
{
  "sys_id": "link_123abc",
  "name": "SW-CORE-01_Port_24",
  "u_name": "Link Principal Datacenter",
  "ip_address": "192.168.10.1",
  "mac_address": "00:1B:44:11:3A:B7",
  "dns_domain": "bradesco.com.br",
  "company": "company_456def",
  "location": "Datacenter São Paulo",
  "u_environment": "Production",
  "port": "GigabitEthernet0/24",
  "speed": "1000",
  "duplex": "Full",
  "operational_status": "1",
  "install_status": "1",
  "u_status": "Active"
}
```

## Tipos de Network Links

### Por Função

```
Core Switch Links      (Conectividade principal)
Access Switch Links    (Acesso usuário final)
Router WAN Links       (Links WAN/Internet)
Firewall Links         (Conectividade firewall)
Load Balancer Links    (Links balanceadores)
```

### Por Tecnologia

```
Ethernet Links         (Conexões Ethernet)
Fiber Optic Links      (Fibra óptica)
Wireless Links         (Conexões sem fio)
VPN Links              (Links VPN)
MPLS Links             (Conexões MPLS)
```

### Por Ambiente

```
Production Links       (Ambiente produção)
Development Links      (Ambiente desenvolvimento)  
Testing Links          (Ambiente testes)
Disaster Recovery      (Links DR)
Management Network     (Rede gerência)
```

## Estratégia UPSERT

### Diferença das Tasks de Incidents

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    upsert_by_sys_id(
        dataset=self.dataset, model=CmdbCiNetworkLink, log=self.log
    )
    return self.log
```

**Vantagens do UPSERT**:
- **Preserva Timestamps**: `etl_created_at` mantém valor original
- **Performance**: Não deleta/recria registros inalterados
- **Histórico**: Mantém auditoria de descoberta de equipamentos
- **Incremental**: Apenas insere novos ou atualiza modificados

### Deduplicação

```python
return pl.DataFrame(
    result_list,
    schema={f.name: pl.String for f in CmdbCiNetworkLink._meta.fields},
).unique(subset="sys_id")
```

**Por que Deduplicar**:
- API do ServiceNow pode retornar duplicatas em queries complexas
- Dot-walk pode resultar em múltiplas referências ao mesmo objeto
- Garante integridade dos dados antes do UPSERT

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Total** | 500-5000 links | Depende do tamanho da infraestrutura |
| **Novos por Execução** | 5-50 links | Crescimento da rede |
| **Modificados** | 10-100 links | Mudanças de configuração |
| **Tempo de Execução** | 30-90 segundos | Dot-walk impacta performance |

### Query Performance

O dot-walk `company.nameLIKEbradesco` adiciona complexidade:

```python
# ⚠️ Mais lento: Com dot-walk (atual)
query = "company.nameLIKEbradesco"

# ✅ Alternativa mais rápida: Buscar companies primeiro
# 1. Buscar IDs de companies Bradesco
# 2. Filtrar links por company_ids: companyIN[id1,id2,id3]
```

**Trade-off**: Precisão vs Performance
- Com dot-walk: Dados precisos, mas mais lento
- Sem dot-walk: Mais rápido, mas precisa filtrar depois

## Uso Prático

### Mapeamento de Topologia

```python
def build_network_topology():
    """Constrói mapeamento da topologia de rede"""
    
    links = CmdbCiNetworkLink.objects.filter(
        operational_status='1',  # Operacional
        install_status='1'       # Instalado
    )
    
    topology = {
        'nodes': {},
        'connections': [],
        'stats': {
            'total_links': links.count(),
            'by_location': {},
            'by_speed': {},
            'by_environment': {}
        }
    }
    
    for link in links:
        # Nós da topologia
        if link.location not in topology['nodes']:
            topology['nodes'][link.location] = {
                'links': [],
                'total_bandwidth': 0
            }
        
        # Adicionar link ao nó
        topology['nodes'][link.location]['links'].append({
            'name': link.name,
            'ip': link.ip_address,
            'speed': link.speed,
            'port': link.port
        })
        
        # Calcular bandwidth total
        if link.speed:
            try:
                speed_mbps = int(link.speed)
                topology['nodes'][link.location]['total_bandwidth'] += speed_mbps
            except (ValueError, TypeError):
                pass
        
        # Estatísticas
        topology['stats']['by_location'].setdefault(link.location, 0)
        topology['stats']['by_location'][link.location] += 1
        
        if link.speed:
            topology['stats']['by_speed'].setdefault(link.speed, 0)
            topology['stats']['by_speed'][link.speed] += 1
        
        if link.u_environment:
            topology['stats']['by_environment'].setdefault(link.u_environment, 0)
            topology['stats']['by_environment'][link.u_environment] += 1
    
    return topology
```

### Análise de Capacidade

```python
def network_capacity_analysis():
    """Análise de capacidade da rede"""
    
    from django.db.models import Count, Q
    
    # Links por velocidade
    speed_distribution = CmdbCiNetworkLink.objects.values('speed').annotate(
        count=Count('sys_id')
    ).order_by('-count')
    
    # Links por status
    status_distribution = CmdbCiNetworkLink.objects.values('operational_status').annotate(
        count=Count('sys_id')
    ).order_by('operational_status')
    
    # Links críticos (alta velocidade)
    high_speed_links = CmdbCiNetworkLink.objects.filter(
        Q(speed='10000') |  # 10Gbps
        Q(speed='40000') |  # 40Gbps  
        Q(speed='100000')   # 100Gbps
    )
    
    # Links com problemas
    problem_links = CmdbCiNetworkLink.objects.filter(
        Q(operational_status__in=['2', '3', '4']) |  # Down, Warning, etc.
        Q(install_status__in=['3', '6', '7'])        # Retired, etc.
    )
    
    return {
        'total_links': CmdbCiNetworkLink.objects.count(),
        'speed_distribution': list(speed_distribution),
        'status_distribution': list(status_distribution),
        'high_speed_count': high_speed_links.count(),
        'problem_links_count': problem_links.count(),
        'health_percentage': calculate_network_health()
    }

def calculate_network_health():
    """Calcula percentual de saúde da rede"""
    total = CmdbCiNetworkLink.objects.count()
    if total == 0:
        return 100
    
    healthy = CmdbCiNetworkLink.objects.filter(
        operational_status='1',  # Operational
        install_status='1'       # Installed
    ).count()
    
    return round((healthy / total) * 100, 1)
```

### Detecção de Mudanças

```python
def detect_network_changes(days_back=7):
    """Detecta mudanças na configuração de rede"""
    
    from datetime import timedelta
    from django.utils import timezone
    
    cutoff_date = timezone.now() - timedelta(days=days_back)
    
    # Links criados recentemente
    new_links = CmdbCiNetworkLink.objects.filter(
        etl_created_at__gte=cutoff_date
    )
    
    # Links modificados recentemente  
    modified_links = CmdbCiNetworkLink.objects.filter(
        etl_updated_at__gte=cutoff_date
    ).exclude(
        etl_created_at__gte=cutoff_date  # Excluir os novos
    )
    
    changes = {
        'new_links': [],
        'modified_links': [],
        'summary': {
            'new_count': new_links.count(),
            'modified_count': modified_links.count()
        }
    }
    
    # Detalhes dos novos links
    for link in new_links:
        changes['new_links'].append({
            'name': link.name,
            'ip_address': link.ip_address,
            'location': link.location,
            'speed': link.speed,
            'created_at': link.etl_created_at.isoformat()
        })
    
    # Detalhes dos links modificados
    for link in modified_links:
        changes['modified_links'].append({
            'name': link.name,
            'ip_address': link.ip_address,
            'location': link.location,
            'updated_at': link.etl_updated_at.isoformat()
        })
    
    return changes
```

## Monitoramento

### Métricas de Infraestrutura

```python
def infrastructure_metrics():
    """Métricas da infraestrutura de rede"""
    
    from django.db.models import Count, Q
    from collections import defaultdict
    
    # Métricas básicas
    total_links = CmdbCiNetworkLink.objects.count()
    active_links = CmdbCiNetworkLink.objects.filter(
        operational_status='1'
    ).count()
    
    # Distribuição por localização
    by_location = defaultdict(int)
    for link in CmdbCiNetworkLink.objects.values('location').annotate(count=Count('sys_id')):
        location = link['location'] or 'Unknown'
        by_location[location] = link['count']
    
    # Distribuição por ambiente
    by_environment = defaultdict(int)
    for link in CmdbCiNetworkLink.objects.values('u_environment').annotate(count=Count('sys_id')):
        env = link['u_environment'] or 'Unknown'
        by_environment[env] = link['count']
    
    # Links críticos sem redundância (identificar SPOFs)
    critical_locations = []
    for location, count in by_location.items():
        if count == 1:  # Apenas um link
            critical_locations.append(location)
    
    return {
        'overview': {
            'total_links': total_links,
            'active_links': active_links,
            'availability_percentage': round((active_links / total_links * 100), 1) if total_links else 0
        },
        'distribution': {
            'by_location': dict(by_location),
            'by_environment': dict(by_environment)
        },
        'risk_analysis': {
            'single_points_of_failure': critical_locations,
            'spof_count': len(critical_locations)
        }
    }
```

### Alertas de Configuração

```python
def configuration_alerts():
    """Alertas de configuração da rede"""
    
    alerts = []
    
    # 1. Links sem IP configurado
    no_ip = CmdbCiNetworkLink.objects.filter(
        Q(ip_address__isnull=True) | Q(ip_address=''),
        operational_status='1'
    ).count()
    
    if no_ip > 0:
        alerts.append({
            'type': 'missing_ip',
            'severity': 'warning',
            'message': f'{no_ip} links ativos sem IP configurado'
        })
    
    # 2. Links duplicados por IP
    duplicate_ips = CmdbCiNetworkLink.objects.values('ip_address').annotate(
        count=Count('sys_id')
    ).filter(count__gt=1, ip_address__isnull=False).exclude(ip_address='')
    
    if duplicate_ips.exists():
        alerts.append({
            'type': 'duplicate_ip',
            'severity': 'error',
            'message': f'{duplicate_ips.count()} IPs duplicados encontrados'
        })
    
    # 3. Links com status inconsistente
    inconsistent = CmdbCiNetworkLink.objects.filter(
        operational_status='1',  # Operacional
        install_status__in=['3', '6', '7']  # Mas não instalado
    ).count()
    
    if inconsistent > 0:
        alerts.append({
            'type': 'status_inconsistency',
            'severity': 'warning', 
            'message': f'{inconsistent} links com status inconsistente'
        })
    
    # 4. Crescimento anormal
    from datetime import timedelta
    from django.utils import timezone
    
    recent_growth = CmdbCiNetworkLink.objects.filter(
        etl_created_at__gte=timezone.now() - timedelta(days=1)
    ).count()
    
    if recent_growth > 50:  # Threshold ajustável
        alerts.append({
            'type': 'unusual_growth',
            'severity': 'info',
            'message': f'{recent_growth} novos links nas últimas 24h'
        })
    
    return alerts
```

## Integração com Incidents

### Análise de Impacto

```python
def network_impact_analysis(incident):
    """Analisa impacto de incident na rede"""
    
    if not incident.u_affected_ci:
        return {'impact_level': 'unknown', 'affected_links': []}
    
    # Buscar links relacionados ao CI afetado
    related_links = CmdbCiNetworkLink.objects.filter(
        Q(name__icontains=incident.u_affected_ci) |
        Q(u_name__icontains=incident.u_affected_ci) |
        Q(location__icontains=incident.u_affected_ci)
    )
    
    if not related_links.exists():
        return {'impact_level': 'isolated', 'affected_links': []}
    
    impact_analysis = {
        'impact_level': 'unknown',
        'affected_links': [],
        'risk_assessment': {
            'total_affected': related_links.count(),
            'critical_affected': 0,
            'locations_impacted': set(),
            'environments_impacted': set()
        }
    }
    
    for link in related_links:
        link_info = {
            'name': link.name,
            'ip_address': link.ip_address,
            'location': link.location,
            'speed': link.speed,
            'environment': link.u_environment,
            'criticality': determine_link_criticality(link)
        }
        
        impact_analysis['affected_links'].append(link_info)
        
        # Coletar dados para avaliação de risco
        if link_info['criticality'] == 'critical':
            impact_analysis['risk_assessment']['critical_affected'] += 1
        
        if link.location:
            impact_analysis['risk_assessment']['locations_impacted'].add(link.location)
        
        if link.u_environment:
            impact_analysis['risk_assessment']['environments_impacted'].add(link.u_environment)
    
    # Determinar nível de impacto
    if impact_analysis['risk_assessment']['critical_affected'] > 0:
        impact_analysis['impact_level'] = 'critical'
    elif len(impact_analysis['risk_assessment']['locations_impacted']) > 2:
        impact_analysis['impact_level'] = 'high'
    elif impact_analysis['risk_assessment']['total_affected'] > 5:
        impact_analysis['impact_level'] = 'medium'
    else:
        impact_analysis['impact_level'] = 'low'
    
    # Converter sets para listas para serialização
    impact_analysis['risk_assessment']['locations_impacted'] = list(
        impact_analysis['risk_assessment']['locations_impacted']
    )
    impact_analysis['risk_assessment']['environments_impacted'] = list(
        impact_analysis['risk_assessment']['environments_impacted']
    )
    
    return impact_analysis

def determine_link_criticality(link):
    """Determina criticidade de um link baseado em características"""
    
    # Links de alta velocidade são críticos
    if link.speed and int(link.speed or 0) >= 10000:  # 10Gbps+
        return 'critical'
    
    # Links de produção são mais críticos
    if link.u_environment and 'prod' in link.u_environment.lower():
        return 'high'
    
    # Links em datacenters principais
    if link.location and any(dc in link.location.lower() for dc in ['datacenter', 'dc', 'core']):
        return 'high'
    
    return 'medium'
```

Esta task é essencial para manter o inventário de conectividade de rede atualizado e possibilitar análises de impacto precisas durante incidents de infraestrutura.