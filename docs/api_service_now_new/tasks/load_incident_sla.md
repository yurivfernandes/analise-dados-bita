# LoadIncidentSla

## Visão Geral

A task `LoadIncidentSla` extrai registros de SLA (Service Level Agreement) associados aos incidents do ServiceNow. Estes dados são cruciais para análise de performance, compliance e métricas de atendimento.

## Características

- **Tipo**: Task de Incidents (com período)
- **Modelo**: `IncidentSla`
- **Filtro Principal**: `sys_created_on` (data de criação do SLA)
- **Estratégia de Carga**: DELETE + INSERT (transacional)
- **Relacionamento**: Conecta com `Incident` via campo `task`

## Implementação

### Classe Principal

```python
class LoadIncidentSla(MixinGetDataset, Pipeline):
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date  # YYYY-MM-DD
        self.end_date = end_date      # YYYY-MM-DD
        super().__init__()
```

### Filtro de Dados

```python
@property
def _filtro(self) -> dict:
    return {
        "sys_created_on__gte": ensure_datetime(self.start_date, end=False),
        "sys_created_on__lte": ensure_datetime(self.end_date, end=True),
    }
```

**Diferença Importante**: Usa `sys_created_on` ao invés de `opened_at` como no LoadIncidentsOpened.

### Query ServiceNow Complexa

```python
query = f"sys_created_on>={self.start_date} 00:00:00^sys_created_on<={self.end_date} 23:59:59^taskISNOTEMPTY"
add_q = "task.assignment_group.nameLIKEvita"
query = f"{query}^{add_q}"
```

**Componentes da Query**:
1. `sys_created_on>=2025-01-20 00:00:00` - Data início
2. `sys_created_on<=2025-01-20 23:59:59` - Data fim  
3. `taskISNOTEMPTY` - SLA deve ter task associado
4. `task.assignment_group.nameLIKEvita` - **Dot-walk**: Filtra pelo grupo do incident relacionado

### Dot-Walk Explanation

O ServiceNow permite "navegar" relacionamentos na query usando dot notation:

```
task.assignment_group.nameLIKEvita
 ↑         ↑           ↑
 |         |           └── Nome do grupo contém "vita"
 |         └── Campo assignment_group do incident
 └── Campo task (referência ao incident)
```

Isso é equivalente a um JOIN em SQL:
```sql
SELECT sla.* FROM task_sla sla
JOIN incident inc ON sla.task = inc.sys_id  
JOIN sys_user_group grp ON inc.assignment_group = grp.sys_id
WHERE grp.name LIKE '%vita%'
```

## Dados Extraídos

### Campos Principais

O modelo `IncidentSla` inclui campos como:

- **Identificação**
  - `sys_id` (PK)
  - `task` (referência ao incident)
  - `sla` (referência ao contrato SLA)

- **Temporização**
  - `start_time` - Início da contagem do SLA
  - `end_time` - Fim esperado do SLA
  - `pause_time` - Tempo pausado
  - `business_pause_duration` - Pausa em horário comercial

- **Status**
  - `stage` - Estágio atual (In Progress, Completed, etc.)
  - `has_breached` - Violou o SLA (true/false)
  - `percentage` - Percentual de cumprimento
  - `business_percentage` - Percentual em horário comercial

- **Auditoria**
  - `sys_created_on`, `sys_created_by`
  - `sys_updated_on`, `sys_updated_by`

### Exemplo de Dados

```json
{
  "sys_id": "sla123abc",
  "task": "inc456def",
  "sla": "contract789",
  "stage": "In Progress", 
  "start_time": "2025-01-20 08:30:00",
  "end_time": "2025-01-20 16:30:00",
  "has_breached": "false",
  "business_percentage": "45.5",
  "percentage": "32.1"
}
```

## Relacionamentos

### Com Incidents

```python
# Via Django ORM (necessário definir relacionamento)
incident = Incident.objects.get(sys_id='inc456def')
slas = IncidentSla.objects.filter(task=incident.sys_id)
```

### Com Contratos SLA

```python
# Buscar detalhes do contrato
contract = ContractSla.objects.get(sys_id=sla.sla)
print(f"SLA: {contract.name}, Duração: {contract.duration}")
```

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Diário** | 1000-5000 SLAs | ~2-5x o número de incidents |
| **Tempo Médio** | 3-8 minutos | Mais lento que incidents devido ao dot-walk |
| **API Calls** | 10-50 requests | Depende do volume |
| **Complexidade Query** | Alta | Dot-walk impacta performance |

### Query Performance

O dot-walk `task.assignment_group.nameLIKEvita` é computacionalmente caro no ServiceNow:

```python
# ✅ Otimizado: Sem dot-walk  
query = "sys_created_on>=2025-01-20^taskISNOTEMPTY"

# ⚠️ Mais lento: Com dot-walk (atual)
query = "sys_created_on>=2025-01-20^taskISNOTEMPTY^task.assignment_group.nameLIKEvita"
```

**Trade-off**: Precisão vs Performance
- Com dot-walk: Dados precisos, mas mais lento
- Sem dot-walk: Mais rápido, mas precisa filtrar depois

## Estratégia de Carga

### Delete + Insert

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    self.load(dataset=self.dataset, model=IncidentSla, filtro=self._filtro)
    return self.log
```

**Vantagem**: Garante consistência com dados que podem mudar (SLAs são atualizados constantemente)

**Processo**:
1. DELETE: Remove SLAs criados no período
2. INSERT: Insere todos os SLAs atuais do período
3. Resultado: Estado atual dos SLAs no ServiceNow

## Uso Prático

### Análise de Cumprimento

```python
# SLAs violados no período
breached = IncidentSla.objects.filter(
    has_breached='true',
    sys_created_on__date='2025-01-20'
)

print(f"SLAs violados: {breached.count()}")

# Performance média
avg_performance = IncidentSla.objects.filter(
    sys_created_on__date='2025-01-20'
).aggregate(
    avg_business=Avg('business_percentage'),
    avg_total=Avg('percentage')
)
```

### Join com Incidents

```python
from django.db import connection

query = """
SELECT i.number, i.priority, s.has_breached, s.business_percentage
FROM incident i
JOIN incident_sla s ON i.sys_id = s.task  
WHERE s.sys_created_on::date = %s
"""

with connection.cursor() as cursor:
    cursor.execute(query, ['2025-01-20'])
    results = cursor.fetchall()
```

## Execução

### Standalone

```python
task = LoadIncidentSla(
    start_date="2025-01-20",
    end_date="2025-01-20"  
)

with task as loader:
    result = loader.run()
    
print(f"SLAs processados: {result['n_inserted']}")
print(f"Duração: {result['duration']}s")
```

### Em Paralelo (View)

Executa simultaneamente com:
- `LoadIncidentsOpened`
- `LoadTaskTimeWorked`  
- `LoadIncidentTask`

```python
# Thread paralela
th = threading.Thread(
    target=_run_task,
    args=("load_incident_sla", LoadIncidentSla, start_date, end_date, results, errors),
    daemon=True
)
th.start()
```

## Monitoramento

### Métricas de Negócio

```python
# Dashboard queries
sla_metrics = {
    'total_slas': IncidentSla.objects.filter(sys_created_on__date=date).count(),
    'breached': IncidentSla.objects.filter(
        sys_created_on__date=date, 
        has_breached='true'
    ).count(),
    'avg_performance': IncidentSla.objects.filter(
        sys_created_on__date=date
    ).aggregate(avg=Avg('business_percentage'))['avg']
}

breach_rate = (sla_metrics['breached'] / sla_metrics['total_slas']) * 100
```

### Alertas

```python
# Alerta se taxa de violação > 10%
if breach_rate > 10:
    send_alert(f"Taxa de violação SLA alta: {breach_rate:.1f}%")

# Alerta se performance média < 80%
if sla_metrics['avg_performance'] < 80:
    send_alert(f"Performance SLA baixa: {sla_metrics['avg_performance']:.1f}%")
```

## Troubleshooting

### Problemas Comuns

**1. Dot-walk timeout**
```
Erro: Query timeout após 30s
Causa: Dot-walk muito complexo
Solução: Simplificar query ou aumentar timeout
```

**2. SLAs órfãos**
```
Situação: SLA.task não existe em Incident
Causa: Incident deletado mas SLA permanece
Solução: Adicionar validação de integridade
```

**3. Performance degradada**
```
Sintoma: Duração > 15 minutos
Causa: Volume alto + dot-walk
Solução: Executar em horários de menor carga
```

### Debug Queries

```python
# Testar query manualmente
from api_service_now_new.utils.servicenow import paginate

# Query simplificada (sem dot-walk)
simple_query = "sys_created_on>=2025-01-20 00:00:00^taskISNOTEMPTY"
result = paginate("task_sla", params={
    "sysparm_query": simple_query,
    "sysparm_limit": "10"
})

print(f"Registros encontrados: {len(result)}")

# Query completa (com dot-walk)  
full_query = f"{simple_query}^task.assignment_group.nameLIKEvita"
# Avaliar diferença de performance
```

## Otimizações Futuras

### Filtragem em Duas Etapas

```python
# 1. Buscar todos os SLAs do período (rápido)
all_slas = paginate("task_sla", params={
    "sysparm_query": "sys_created_on>=2025-01-20^taskISNOTEMPTY"
})

# 2. Filtrar por assignment_group localmente
vita_incidents = set(Incident.objects.filter(
    assignment_group__contains='vita'
).values_list('sys_id', flat=True))

filtered_slas = [
    sla for sla in all_slas 
    if sla.get('task') in vita_incidents
]
```

### Cache de Relationships

```python
# Cache grupos Vita para evitar dot-walk repetido
VITA_GROUPS = Groups.objects.filter(
    name__icontains='vita'
).values_list('sys_id', flat=True)

# Usar nos filtros
group_filter = "^OR".join([f"task.assignment_group={gid}" for gid in VITA_GROUPS])
```

Esta task é essencial para análises de SLA e requer atenção especial devido à complexidade das queries com dot-walk.