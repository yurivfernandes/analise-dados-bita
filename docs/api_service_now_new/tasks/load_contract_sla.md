# LoadContractSla

## Visão Geral

A task `LoadContractSla` extrai definições de contratos SLA do ServiceNow. Estes contratos definem as métricas de tempo de resposta e resolução que devem ser cumpridas para diferentes tipos de incidents e requests.

## Características

- **Tipo**: Task de Configurações (sem período)
- **Modelo**: `ContractSla`
- **Filtro Principal**: Nome do contrato
- **Estratégia de Carga**: UPSERT (preserva timestamps ETL)
- **Frequência**: Dados relativamente estáticos, executados esporadicamente

## Implementação

### Classe Principal

```python
class LoadContractSla(MixinGetDataset, Pipeline):
    def __init__(self):
        super().__init__()
        # Não recebe parâmetros de data
```

### Query ServiceNow

```python
add_q = "nameLIKE[vita^ORnameLIKE[vgr^ORnameLIKEbradesco"
params = {"sysparm_fields": fields, "sysparm_query": add_q}
```

**Filtros Aplicados**:
- `nameLIKE[vita` - Contratos com "vita" no nome
- `ORnameLIKE[vgr` - OU contratos com "vgr" no nome  
- `ORnameLIKEbradesco` - OU contratos com "bradesco" no nome

**Diferença das Tasks de Incidents**: Não filtra por data, busca todos os contratos ativos.

## Estrutura de Contratos SLA

### Campos Principais

**Identificação**:
- `sys_id` (PK) - ID único do contrato
- `name` - Nome do contrato SLA
- `description` - Descrição detalhada

**Definições de Tempo**:
- `duration` - Duração do SLA (formato: duração em segundos)  
- `schedule` - Cronograma aplicável (24x7, horário comercial, etc.)

**Condições**:
- `start_condition` - Condição para início da contagem
- `stop_condition` - Condição para parada da contagem
- `pause_condition` - Condição para pausar a contagem

**Workflow**:
- `workflow` - Workflow associado ao SLA
- `script` - Script executado no SLA

**Status**:
- `active` - Contrato ativo (true/false)
- `advanced` - SLA avançado (true/false)

### Exemplo de Contrato

```json
{
  "sys_id": "sla_contract_123",
  "name": "Vita - Priority 1 - Resolution",
  "description": "SLA de resolução para incidents Priority 1 da Vita - 4 horas em horário comercial",
  "duration": "14400000",  // 4 horas em milissegundos
  "schedule": "business_hours_vita",
  "start_condition": "priority=1^state=2",  // Priority 1 E In Progress
  "stop_condition": "state=6^ORstate=7",    // Resolved OU Closed
  "pause_condition": "state=3",             // Pending
  "active": "true",
  "advanced": "false"
}
```

## Tipos de Contratos Típicos

### Por Prioridade

```
Vita - Priority 1 - Response    (15 min resposta)
Vita - Priority 1 - Resolution  (4h resolução)
Vita - Priority 2 - Response    (1h resposta)  
Vita - Priority 2 - Resolution  (8h resolução)
Vita - Priority 3 - Response    (4h resposta)
Vita - Priority 3 - Resolution  (24h resolução)
```

### Por Tipo de Serviço

```
Vita - Critical Infrastructure  (30 min resolução)
Vita - Standard Request        (5 dias resolução)
Vita - Emergency Change        (2h aprovação)
```

### Por Cliente

```
Bradesco - P1 Resolution       (2h resolução)
VGR - Standard Response        (2h resposta)  
Vita Internal - P1 Resolution  (4h resolução)
```

## Estratégia UPSERT

### Diferença das Tasks de Incidents

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    # USA upsert_by_sys_id ao invés de self.load()
    upsert_by_sys_id(dataset=self.dataset, model=ContractSla, log=self.log)
    return self.log
```

**Vantagens do UPSERT**:
- **Preserva Timestamps**: `etl_created_at` mantém valor original
- **Performance**: Não deleta/recria registros inalterados
- **Histórico**: Mantém auditoria de quando cada contrato foi criado
- **Incremental**: Apenas insere novos ou atualiza modificados

### Processo UPSERT

```python
# 1. Busca contratos existentes no banco
existing = {o.sys_id: o for o in ContractSla.objects.filter(sys_id__in=[...])}

# 2. Separa operações
to_create = []  # Novos contratos
to_update = []  # Contratos existentes modificados

# 3. Para cada contrato do ServiceNow
for contract_data in dataset:
    if contract_data['sys_id'] in existing:
        # Atualiza existente
        obj = existing[contract_data['sys_id']]
        for field, value in contract_data.items():
            setattr(obj, field, value)
        to_update.append(obj)
    else:
        # Cria novo
        to_create.append(ContractSla(**contract_data))

# 4. Executa bulk operations
ContractSla.objects.bulk_create(to_create, batch_size=1000)
ContractSla.objects.bulk_update(to_update, fields, batch_size=1000)
```

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Total** | 50-200 contratos | Dados relativamente estáticos |
| **Novos por Execução** | 0-5 contratos | Raramente criados |
| **Modificados** | 5-20 contratos | Ocasionalmente ajustados |
| **Tempo de Execução** | 10-30 segundos | Muito mais rápido que incidents |

### Frequência de Execução

```python
# ✅ Recomendado: Diário ou semanal
# Contratos SLA mudam pouco

# ⚠️ Aceitável: Durante carga de incidents  
# Para garantir contratos atualizados

# ❌ Desnecessário: Múltiplas vezes por dia
# Waste de recursos para dados estáticos
```

## Uso Prático

### Análise de SLA Configuration

```python
# Contratos por cliente
contracts_by_client = {}
for contract in ContractSla.objects.filter(active='true'):
    if 'vita' in contract.name.lower():
        client = 'Vita'
    elif 'bradesco' in contract.name.lower():
        client = 'Bradesco'
    elif 'vgr' in contract.name.lower():
        client = 'VGR'
    else:
        client = 'Other'
    
    contracts_by_client.setdefault(client, []).append(contract)

# Durações médias por prioridade
priority_durations = {}
for contract in ContractSla.objects.filter(active='true'):
    if 'priority 1' in contract.name.lower():
        priority = 'P1'
    elif 'priority 2' in contract.name.lower():
        priority = 'P2'
    elif 'priority 3' in contract.name.lower():
        priority = 'P3'
    else:
        continue
        
    duration_hours = int(contract.duration) / (1000 * 3600) if contract.duration else 0
    priority_durations.setdefault(priority, []).append(duration_hours)
```

### Join com IncidentSla

```python
# SLAs ativos e seus contratos
from django.db import connection

query = """
SELECT 
    c.name as contract_name,
    c.duration,
    COUNT(s.sys_id) as active_slas,
    COUNT(CASE WHEN s.has_breached = 'true' THEN 1 END) as breached_count
FROM contract_sla c
LEFT JOIN incident_sla s ON c.sys_id = s.sla
WHERE c.active = 'true'
  AND s.sys_created_on::date = %s
GROUP BY c.sys_id, c.name, c.duration
ORDER BY active_slas DESC
"""

with connection.cursor() as cursor:
    cursor.execute(query, ['2025-01-20'])
    results = cursor.fetchall()
    
for row in results:
    contract_name, duration, active_slas, breached = row
    breach_rate = (breached / active_slas * 100) if active_slas > 0 else 0
    print(f"{contract_name}: {active_slas} SLAs, {breach_rate:.1f}% breached")
```

## Configuração e Filtros

### Filtros Customizáveis

O filtro atual é hardcoded:

```python
add_q = "nameLIKE[vita^ORnameLIKE[vgr^ORnameLIKEbradesco"
```

**Possível Melhoria**:

```python
# Em settings.py
SERVICENOW_SLA_FILTERS = [
    'vita',
    'vgr', 
    'bradesco',
    'internal'
]

# Na task
filter_conditions = [f"nameLIKE{client}" for client in settings.SERVICENOW_SLA_FILTERS]
add_q = "^OR".join(filter_conditions)
```

### Campos Extraídos

```python
fields = ",".join([
    f.name for f in ContractSla._meta.fields 
    if not f.name.startswith("etl_") and f.name != "etl_hash"
])

# Campos típicos incluídos:
# sys_id, name, description, duration, schedule,
# start_condition, stop_condition, pause_condition,
# workflow, script, active, advanced, etc.
```

## Monitoramento

### Métricas de Configuração

```python
from django.utils import timezone
from datetime import timedelta

# Contratos criados/modificados recentemente  
recent_changes = ContractSla.objects.filter(
    etl_updated_at__gte=timezone.now() - timedelta(days=7)
)

print(f"Contratos modificados na última semana: {recent_changes.count()}")

# Contratos por status
active_count = ContractSla.objects.filter(active='true').count()
inactive_count = ContractSla.objects.filter(active='false').count()

print(f"Contratos ativos: {active_count}")
print(f"Contratos inativos: {inactive_count}")

# Distribuição de durações
durations = ContractSla.objects.filter(
    active='true',
    duration__isnull=False
).values_list('duration', flat=True)

duration_hours = [int(d)/(1000*3600) for d in durations if d]
avg_duration = sum(duration_hours) / len(duration_hours) if duration_hours else 0

print(f"Duração média dos SLAs: {avg_duration:.1f} horas")
```

### Alertas de Configuração

```python
# Alerta: muitos contratos inativos
if inactive_count > active_count * 0.3:  # >30% inativos
    send_alert(f"Muitos contratos SLA inativos: {inactive_count}/{active_count+inactive_count}")

# Alerta: contratos sem duração definida
no_duration = ContractSla.objects.filter(
    active='true',
    duration__isnull=True
).count()

if no_duration > 0:
    send_alert(f"Contratos SLA ativos sem duração definida: {no_duration}")
```

## Execução

### Standalone

```python
task = LoadContractSla()

with task as loader:
    result = loader.run()
    
print(f"Contratos processados: {result.get('n_inserted', 0)}")
print(f"Duração: {result['duration']}s")

# Resultado típico:
# Contratos processados: 3  (apenas novos/modificados)
# Duração: 15.2s
```

### Em Lote com Outras Configurações

```python
# LoadConfigurationsView executa em lotes de 3
batch1 = [
    ("load_contract_sla", LoadContractSla),      # Esta task
    ("load_groups", LoadGroups),
    ("load_sys_company", LoadSysCompany),
]

# Execução paralela do lote
threads = []
for name, cls in batch1:
    thread = threading.Thread(
        target=execute_config_task,
        args=(name, cls),
        daemon=True
    )
    thread.start()
    threads.append(thread)

# Aguarda conclusão do lote
for thread in threads:
    thread.join()
```

## Troubleshooting

### Problemas Comuns

**1. Filtro muito restritivo**
```
Situação: n_inserted = 0 sempre
Causa: Nomes dos contratos mudaram no ServiceNow
Solução: Revisar filtros "nameLIKE[..."
```

**2. Contratos órfãos em IncidentSla**
```
Situação: IncidentSla.sla não existe em ContractSla
Causa: Contrato deletado no ServiceNow
Investigação: Verificar se filtro exclui contratos necessários
```

**3. Performance degradada**
```
Sintoma: Duração > 2 minutos
Causa: Muitos contratos novos/modificados
Normal: Ocorre após mudanças em massa no ServiceNow
```

### Debug

```python
# Testar filtro manualmente
from api_service_now_new.utils.servicenow import paginate

# Query atual
query = "nameLIKE[vita^ORnameLIKE[vgr^ORnameLIKEbradesco"
result = paginate("contract_sla", params={
    "sysparm_query": query,
    "sysparm_limit": "10"
})

print(f"Contratos encontrados: {len(result)}")
for contract in result[:3]:
    print(f"- {contract['name']}")

# Verificar se existem contratos não capturados
all_contracts = paginate("contract_sla", params={"sysparm_limit": "100"})
captured_names = {c['name'] for c in result}
all_names = {c['name'] for c in all_contracts}
missing = all_names - captured_names

if missing:
    print(f"Contratos não capturados: {missing}")
```

## Integração

### Dependências

- **Usado por**: `IncidentSla` (referência via campo `sla`)
- **Independente de**: Outras tasks (pode executar isoladamente)
- **Frequência**: Pode executar menos que tasks de incidents

### Validação de Integridade

```python
def validate_contract_usage():
    """Verifica se todos os contratos referenciados existem"""
    
    # Contratos referenciados em SLAs
    used_contracts = set(IncidentSla.objects.filter(
        sla__isnull=False
    ).values_list('sla', flat=True).distinct())
    
    # Contratos existentes
    existing_contracts = set(ContractSla.objects.values_list('sys_id', flat=True))
    
    # Contratos faltando
    missing = used_contracts - existing_contracts
    
    if missing:
        logger.warning(f"Contratos SLA referenciados mas não existentes: {len(missing)}")
        logger.debug(f"IDs faltando: {missing}")
    
    return len(missing)
```

Esta task é essencial para manter as definições de SLA atualizadas e garantir que análises de performance tenham dados de referência corretos.