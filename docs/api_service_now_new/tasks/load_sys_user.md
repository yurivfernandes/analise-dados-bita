# LoadSysUser

## Visão Geral

A task `LoadSysUser` extrai dados de usuários do ServiceNow, mas com uma abordagem inteligente: ao invés de buscar todos os usuários (que seriam milhares), ela identifica apenas os usuários que estão referenciados nos incidents já carregados e busca seus dados individualmente.

## Características

- **Tipo**: Task de Configurações (sem período)
- **Modelo**: `SysUser`
- **Estratégia Única**: Busca baseada em referências de incidents
- **Método de Extração**: Múltiplas chamadas individuais (`fetch_single_record`)
- **Estratégia de Carga**: UPSERT (preserva timestamps ETL)

## Implementação

### Classe Principal

```python
class LoadSysUser(MixinGetDataset, Pipeline):
    def __init__(self):
        super().__init__()
        # Não recebe parâmetros - lógica baseada em dados existentes
```

### Estratégia Inteligente de Busca

Ao invés de uma query genérica, a task:

1. **Identifica usuários referenciados** nos incidents
2. **Busca dados individuais** de cada usuário
3. **Evita download desnecessário** de milhares de usuários

```python
@property
def _users(self) -> pl.DataFrame:
    # 1. IDs únicos de usuários presentes em Incident
    opened = Incident.objects.exclude(opened_by__isnull=True).exclude(opened_by="").values_list("opened_by", flat=True).distinct()
    
    resolved = Incident.objects.exclude(resolved_by__isnull=True).exclude(resolved_by="").values_list("resolved_by", flat=True).distinct()
    
    closed = Incident.objects.exclude(closed_by__isnull=True).exclude(closed_by="").values_list("closed_by", flat=True).distinct()

    # 2. União de todos os IDs únicos
    ids: List[str] = sorted({*opened, *resolved, *closed})

    # 3. Busca individual de cada usuário
    all_results: List[Dict] = []
    for sid in ids:
        rec = fetch_single_record(
            path="sys_user", 
            sys_id=sid, 
            params={"sysparm_fields": fields}
        )
        if rec:
            all_results.append(rec)

    return pl.DataFrame(all_results, schema={f.name: pl.String for f in SysUser._meta.fields})
```

### Campos de Referência em Incidents

A task busca usuários referenciados em:

- **`opened_by`**: Quem abriu o incident
- **`resolved_by`**: Quem resolveu o incident  
- **`closed_by`**: Quem fechou o incident

**Nota**: Poderia incluir também `assigned_to`, `caller_id` se necessário.

## Vantagens da Abordagem

### Performance Otimizada

```python
# ❌ Abordagem tradicional (ineficiente):
# Buscar TODOS os usuários do ServiceNow (10k-100k users)
all_users = paginate("sys_user", params={"sysparm_query": "active=true"})

# ✅ Abordagem atual (otimizada):
# Buscar apenas usuários relevantes (~100-500 users)
relevant_user_ids = get_incident_user_references()
relevant_users = [fetch_single_record("sys_user", uid) for uid in relevant_user_ids]
```

### Métricas Comparativas

| Abordagem | Users Baixados | Tempo | Relevância |
|-----------|----------------|-------|------------|
| **Todos os usuários** | 10.000-100.000 | 10-60 min | ~5% relevantes |
| **Apenas referenciados** | 100-500 | 1-3 min | 100% relevantes |

## Estrutura de Dados

### Campos de Usuário

**Identificação**:
- `sys_id` (PK) - ID único do usuário
- `user_name` - Nome de login (ex: joao.silva)
- `employee_number` - Número do funcionário

**Nome Completo**:
- `first_name` - Primeiro nome
- `last_name` - Sobrenome
- `name` - Nome completo (geralmente first_name + last_name)

**Contato**:
- `email` - Email corporativo
- `phone` - Telefone
- `mobile_phone` - Celular

**Organizacional**:
- `department` - Departamento
- `company` - Empresa
- `location` - Localização física
- `manager` - Gerente (referência a outro user)
- `cost_center` - Centro de custo

**Status**:
- `active` - Usuário ativo (true/false)
- `locked_out` - Conta bloqueada
- `failed_attempts` - Tentativas de login falhadas

### Exemplo de Usuário

```json
{
  "sys_id": "user123abc",
  "user_name": "joao.silva",
  "employee_number": "12345",
  "first_name": "João",
  "last_name": "Silva",
  "name": "João Silva",
  "email": "joao.silva@empresa.com",
  "phone": "+55 11 1234-5678",
  "department": "TI - Infrastructure",
  "company": "comp456def",
  "location": "loc789ghi", 
  "manager": "mgr321xyz",
  "active": "true",
  "locked_out": "false",
  "sys_created_on": "2023-01-15 14:30:00",
  "sys_updated_on": "2025-01-18 16:45:00"
}
```

## Fetch Individual Implementation

### fetch_single_record Function

```python
def fetch_single_record(path: str, sys_id: str, params: Optional[Dict] = None, timeout: int = 30) -> Optional[Dict]:
    """
    Busca um único registro no ServiceNow por sys_id.
    
    - Constrói query: sysparm_query=sys_id={sys_id}
    - Limit: 1 registro
    - Timeout: 30 segundos
    - Retorna: Dict do usuário ou None se não encontrado
    """
    params = dict(params or {})
    params.update({"sysparm_query": f"sys_id={sys_id}", "sysparm_limit": "1"})

    base_url, auth, headers = get_servicenow_env()
    url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    resp = requests.get(url, auth=auth, headers=headers, params=params, timeout=timeout)
    
    if resp.status_code == 404:
        return None
    resp.raise_for_status()

    body = resp.json()
    result = body.get("result")
    if not result:
        return None
        
    return process_data([result[0]])[0]  # Processa referências
```

### Tratamento de Usuários Não Encontrados

```python
# Se usuário foi deletado/inativado no ServiceNow
for sid in ids:
    rec = fetch_single_record("sys_user", sys_id=sid, params={"sysparm_fields": fields})
    if rec:
        all_results.append(rec)
    else:
        logger.warning(f"User not found: {sid}")
        # Continua para próximo usuário
```

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Usuários Únicos** | 100-500 | Baseado em incidents existentes |
| **API Calls** | 100-500 | Uma por usuário |
| **Tempo Total** | 1-3 minutos | Depende de latência da API |
| **Taxa de Encontrados** | 95-99% | Alguns usuários podem ser deletados |

### Otimizações Possíveis

**1. Chunking com IN clause** (não implementado):

```python
# Atual: Uma chamada por usuário
for user_id in user_ids:
    user = fetch_single_record("sys_user", user_id)

# Otimização futura: Batch de usuários
def fetch_users_batch(user_ids, batch_size=100):
    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i+batch_size]
        query = "^OR".join([f"sys_id={uid}" for uid in batch])
        yield paginate("sys_user", params={"sysparm_query": query})
```

**2. Cache de usuários frequentes**:

```python
# Usuários que aparecem em muitos incidents
frequent_users = Counter(user_ids).most_common(50)
# Manter cache local desses usuários
```

## Relacionamentos e Análises

### Join com Incidents

```python
# Usuários mais ativos (abrem mais incidents)
from django.db.models import Count

most_active_openers = Incident.objects.values('opened_by').annotate(
    incident_count=Count('sys_id')
).order_by('-incident_count')[:10]

for item in most_active_openers:
    if item['opened_by']:
        user = SysUser.objects.filter(sys_id=item['opened_by']).first()
        user_name = user.name if user else f"ID: {item['opened_by']}"
        print(f"{user_name}: {item['incident_count']} incidents abertos")
```

### Análise de Resolução por Usuário

```python
# Usuários que mais resolvem incidents
top_resolvers = Incident.objects.exclude(resolved_by__isnull=True).values('resolved_by').annotate(
    resolved_count=Count('sys_id')
).order_by('-resolved_count')[:10]

for item in top_resolvers:
    user = SysUser.objects.filter(sys_id=item['resolved_by']).first()
    if user:
        print(f"{user.name} ({user.department}): {item['resolved_count']} incidents resolvidos")
```

### Hierarquia de Managers

```python
def get_manager_hierarchy(user_sys_id, levels=3):
    """Busca hierarquia de gerentes até N níveis"""
    hierarchy = []
    current_id = user_sys_id
    
    for level in range(levels):
        user = SysUser.objects.filter(sys_id=current_id).first()
        if not user:
            break
            
        hierarchy.append({
            'level': level,
            'name': user.name,
            'department': user.department,
            'email': user.email
        })
        
        # Próximo nível: manager
        if user.manager and user.manager != current_id:
            current_id = user.manager
        else:
            break
    
    return hierarchy

# Exemplo de uso
hierarchy = get_manager_hierarchy("user123abc")
for item in hierarchy:
    print(f"Level {item['level']}: {item['name']} - {item['department']}")
```

## Execução

### Standalone

```python
task = LoadSysUser()

with task as loader:
    result = loader.run()
    
print(f"Usuários processados: {result.get('n_inserted', 0)}")
print(f"Duração: {result['duration']}s")

# Log típico:
# Usuários processados: 15  (apenas novos/modificados)
# Duração: 125.6s
```

### Dependência de Dados

```python
# IMPORTANTE: Executar APÓS LoadIncidentsOpened
# Para garantir que incidents existem para referenciar usuários

execution_order = [
    "load_incidents_opened",    # 1º - Cria incidents
    "load_sys_user",           # 2º - Busca usuários dos incidents
    "análises_e_relatórios"    # 3º - Join incidents + users
]
```

### Em Lote (LoadConfigurationsView)

```python
# Lote 2: Executado após contratos/grupos/empresas
batch2 = [
    ("load_sys_user", LoadSysUser),           # Esta task
    ("load_cmdb_ci_network_link", LoadCmdbCiNetworkLink),
]

# Execução em paralelo (2 threads)
for name, cls in batch2:
    thread = threading.Thread(
        target=execute_config_task,
        args=(name, cls),
        daemon=True
    )
    thread.start()
    threads.append(thread)
```

## Monitoramento

### Métricas de Usuários

```python
from collections import Counter

# Distribuição por departamento
users_by_dept = SysUser.objects.values('department').annotate(
    user_count=Count('sys_id')
).order_by('-user_count')

print("Usuários por departamento:")
for dept in users_by_dept[:10]:
    print(f"  {dept['department']}: {dept['user_count']} usuários")

# Usuários inativos referenciados
inactive_referenced = SysUser.objects.filter(
    active='false',
    sys_id__in=Incident.objects.values_list('opened_by', flat=True).distinct()
)

if inactive_referenced.exists():
    print(f"Usuários inativos ainda referenciados: {inactive_referenced.count()}")

# Usuários não encontrados (órfãos)
referenced_users = set()
for field in ['opened_by', 'resolved_by', 'closed_by']:
    ids = Incident.objects.exclude(**{f"{field}__isnull": True}).exclude(**{f"{field}": ""}).values_list(field, flat=True).distinct()
    referenced_users.update(ids)

existing_users = set(SysUser.objects.values_list('sys_id', flat=True))
missing_users = referenced_users - existing_users

if missing_users:
    print(f"Usuários referenciados mas não encontrados: {len(missing_users)}")
```

### Alertas

```python
# Alerta: muitos usuários não encontrados
missing_rate = len(missing_users) / len(referenced_users) * 100 if referenced_users else 0
if missing_rate > 5:
    send_alert(f"Taxa alta de usuários não encontrados: {missing_rate:.1f}%")

# Alerta: tempo de execução alto
if result['duration'] > 300:  # 5 minutos
    send_alert(f"LoadSysUser demorou {result['duration']}s - verificar latência API")
```

## Troubleshooting

### Problemas Comuns

**1. Muitos usuários não encontrados**
```
Situação: 20% dos user_ids retornam None
Causa: Usuários deletados/desativados no ServiceNow
Solução: Normal, apenas registrar no log
```

**2. Timeout em fetch_single_record**
```
Erro: requests.exceptions.ReadTimeout
Causa: API ServiceNow lenta
Solução: Aumentar timeout ou reduzir paralelismo
```

**3. Usuários duplicados em incidents**
```
Situação: Mesmo sys_id em opened_by, resolved_by
Otimização: set() já elimina duplicatas
```

### Debug

```python
# Verificar distribuição de usuários por campo
incident_user_distribution = {
    'opened_by': Incident.objects.exclude(opened_by__isnull=True).exclude(opened_by="").count(),
    'resolved_by': Incident.objects.exclude(resolved_by__isnull=True).exclude(resolved_by="").count(),
    'closed_by': Incident.objects.exclude(closed_by__isnull=True).exclude(closed_by="").count(),
}

print("Incidents com usuários preenchidos:")
for field, count in incident_user_distribution.items():
    print(f"  {field}: {count}")

# Testar fetch individual
test_user_id = Incident.objects.exclude(opened_by__isnull=True).first().opened_by
test_user = fetch_single_record("sys_user", test_user_id)
print(f"Teste fetch usuário {test_user_id}: {'OK' if test_user else 'FALHOU'}")
```

## Melhorias Futuras

### Batch Loading

```python
def fetch_users_in_batches(user_ids, batch_size=50):
    """Busca usuários em lotes usando OR query"""
    all_users = []
    
    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i+batch_size]
        or_conditions = [f"sys_id={uid}" for uid in batch]
        query = "^OR".join(or_conditions)
        
        batch_users = paginate("sys_user", params={
            "sysparm_query": query,
            "sysparm_fields": fields
        })
        
        all_users.extend(batch_users)
    
    return all_users
```

### Campos Adicionais

```python
# Incluir também assigned_to e caller_id
all_user_fields = ['opened_by', 'resolved_by', 'closed_by', 'assigned_to', 'caller_id']

ids = set()
for field in all_user_fields:
    field_ids = Incident.objects.exclude(**{f"{field}__isnull": True}).exclude(**{f"{field}": ""}).values_list(field, flat=True).distinct()
    ids.update(field_ids)
```

Esta task demonstra uma abordagem inteligente para extrair apenas dados necessários, otimizando performance e relevância dos dados extraídos.