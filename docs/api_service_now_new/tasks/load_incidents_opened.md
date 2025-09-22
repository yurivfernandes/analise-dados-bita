# LoadIncidentsOpened

## Visão Geral

A task `LoadIncidentsOpened` é responsável por extrair incidents do ServiceNow que foram abertos em um período específico. É uma das tasks mais críticas do sistema, servindo como base para análises de volume de incidents e tendências de abertura.

## Características

- **Tipo**: Task de Incidents (com período)
- **Modelo**: `Incident`
- **Filtro Principal**: `opened_at` (data de abertura)
- **Estratégia de Carga**: DELETE + INSERT (transacional)
- **Paralelização**: Executa junto com outras 3 tasks de incidents

## Implementação

### Classe Principal

```python
class LoadIncidentsOpened(MixinGetDataset, Pipeline):
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
        "opened_at__gte": ensure_datetime(self.start_date, end=False),
        "opened_at__lte": ensure_datetime(self.end_date, end=True),
    }
```

**Conversão**:
- `start_date: "2025-01-20"` → `"2025-01-20 00:00:00"`
- `end_date: "2025-01-20"` → `"2025-01-20 23:59:59"`

### Query ServiceNow

A task constrói uma query complexa para o ServiceNow:

```python
query = f"opened_at>={start_ts}^opened_at<={end_ts}"
add_q = "assignment_groupLIKEvita"
query = f"{query}^{add_q}"
```

**Tradução**:
- `opened_at>=2025-01-20 00:00:00`
- `^opened_at<=2025-01-20 23:59:59` 
- `^assignment_groupLIKEvita`

Isso significa: incidents abertos no período E com grupo de atribuição contendo "vita".

### Campos Extraídos

Extrai todos os campos definidos no modelo `Incident`, exceto ETL:

```python
fields = ",".join([
    f.name for f in Incident._meta.fields 
    if not f.name.startswith("etl_") and f.name != "etl_hash"
])
```

**Campos incluídos** (~40 campos):
- `sys_id`, `number`, `state`, `incident_state`
- `priority`, `urgency`, `impact`, `severity`
- `category`, `subcategory`, `u_subcategory_detail`
- `assignment_group`, `assigned_to`, `caller_id`
- `opened_at`, `resolved_at`, `closed_at`
- `short_description`, `description`, `close_notes`
- E mais...

### Processamento de Dados

1. **Paginação**: Busca dados em chunks de 10.000 registros
2. **Transformação**: Cria Polars DataFrame com schema tipado
3. **Normalização**: Campos de referência são achatados automaticamente
4. **Limpeza**: Strings vazias convertidas para `None`

### Exemplo de Transformação

**ServiceNow API Response**:
```json
{
  "sys_id": "abc123",
  "assignment_group": {
    "value": "def456",
    "display_value": "Vita Infrastructure"
  },
  "state": "2"
}
```

**Após Processamento**:
```json
{
  "sys_id": "abc123",
  "assignment_group": "def456",
  "dv_assignment_group": "Vita Infrastructure", 
  "state": "2",
  "etl_created_at": "2025-01-20T10:15:30.123456Z",
  "etl_updated_at": "2025-01-20T10:15:30.123456Z"
}
```

## Estratégia de Carga

### Delete + Insert Transacional

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    self.load(dataset=self.dataset, model=Incident, filtro=self._filtro)
    return self.log
```

**Processo**:
1. **DELETE**: Remove incidents existentes no período
2. **INSERT**: Insere todos os registros extraídos
3. **Transação**: Rollback automático em caso de erro

### Vantagens

- **Consistência**: Garante que não há dados duplicados
- **Simplicidade**: Lógica straightforward
- **Confiabilidade**: Remove incidents que possam ter sido deletados no ServiceNow

### Desvantagens

- **Performance**: Reinsere dados inalterados
- **Timestamps ETL**: Perde histórico de criação original

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Diário** | 500-2000 incidents | Varia por dia da semana |
| **Tempo Médio** | 2-5 minutos | Depende do volume |
| **API Calls** | 5-20 requests | 10k registros/page |
| **Tamanho Dataset** | 50-200 MB | Em memória (Polars) |

### Otimizações Implementadas

```python
# Paginação otimizada
result_list = paginate(
    path="incident",
    params=params,
    mode="offset",
    limit=10000,        # Máximo do ServiceNow
    offset_param="sysparm_offset",
    result_key="result"
)

# Bulk insert
objs = [Incident(**vals) for vals in dataset.to_dicts()]
bulk = Incident.objects.bulk_create(objs=objs, batch_size=1000)
```

## Uso e Execução

### Execução Standalone

```python
from api_service_now_new.tasks import LoadIncidentsOpened

# Carregar incidents de hoje
task = LoadIncidentsOpened(
    start_date="2025-01-20", 
    end_date="2025-01-20"
)

with task as loader:
    result = loader.run()
    
print(f"Inseridos: {result['n_inserted']} incidents")
print(f"Deletados: {result['n_deleted']} incidents")  
print(f"Duração: {result['duration']} segundos")
```

### Execução via View (Threading)

```python
# LoadIncidentsView._run_pipelines_in_background
heavy_tasks = [
    ("load_incidents_opened", LoadIncidentsOpened),
    ("load_incident_sla", LoadIncidentSla),
    ("load_task_time_worked", LoadTaskTimeWorked), 
    ("load_incident_task", LoadIncidentTask),
]

# Execução paralela
threads = []
for name, cls in heavy_tasks:
    th = threading.Thread(
        target=_run_task_local, 
        args=(name, cls), 
        daemon=True
    )
    th.start()
    threads.append(th)

for th in threads:
    th.join()  # Aguarda conclusão
```

### Execução Assíncrona (Celery)

```python
from api_service_now_new.tasks.load_incidents_opened import load_incidents_opened_async

# Execução assíncrona
task_result = load_incidents_opened_async.delay(
    start_date="2025-01-20",
    end_date="2025-01-20"
)

# Aguardar resultado
result = task_result.get(timeout=600)  # 10 minutos
print(f"Task ID: {task_result.id}")
print(f"Status: {task_result.status}")
```

## Logging e Monitoramento

### Log Detalhado

```python
{
    "n_inserted": 1250,
    "n_deleted": 1180,
    "started_at": "2025-01-20T10:00:00.000Z",
    "finished_at": "2025-01-20T10:03:45.123Z", 
    "duration": 225.12,
    "delete_duration": 12.34,
    "save_duration": 189.78,
    "load_duration": 202.12
}
```

### Saída Console

```
[Incidents] Executando tarefa: load_incidents_opened (2025-01-20 -> 2025-01-20)
...LIMPANDO OS DADOS DO MODEL [Incident] NO BANCO DE DADOS ...
....FILTROS UTILIZADOS: {'opened_at__gte': '2025-01-20 00:00:00', 'opened_at__lte': '2025-01-20 23:59:59'}...
...1180 DADOS DELETADOS NO BANCO DE DADOS...
...DELETE DURATION: 12.34s...
...SALVANDO OS DADOS NO BANCO DE DADOS NO MODEL: [Incident]...
...1250 REGISTROS SALVOS NO BANCO DE DADOS...
...SAVE DURATION: 189.78s...
...LOAD DURATION: 202.12s (delete+save)...
[Incidents] Concluída: load_incidents_opened em 03:45
```

## Tratamento de Erros

### Erros Comuns

1. **API ServiceNow**
   - Timeout (>30s por request)
   - Rate limiting (muitas requests)
   - Query inválida

2. **Transformação**
   - Schema inconsistente
   - Campos faltando
   - Tipos inválidos

3. **Banco de Dados**
   - Connection timeout
   - Lock timeout em DELETE
   - Constraints violation

### Estratégias de Recuperação

```python
try:
    with LoadIncidentsOpened(start_date=start_date, end_date=end_date) as load:
        r = load.run()
    results[task_name] = r
    logger.info("%s finished: %s", task_name, r)
except Exception as e:
    logger.exception("Erro na task %s", task_name)
    errors.append((task_name, str(e)))
    # Task falha, mas outras continuam executando
```

## Configuração

### Variáveis de Ambiente

```bash
# ServiceNow API
SERVICE_NOW_BASE_URL="https://vitainstance.service-now.com/api/now/table"
SERVICE_NOW_USERNAME="integration_user"
SERVICE_NOW_USER_PASSWORD="secure_password"

# Performance
SERVICENOW_PAGE_SIZE="10000"
DATABASE_BATCH_SIZE="1000"
API_TIMEOUT="30"
```

### Filtros Customizáveis

```python
# Filtro atual (hardcoded)
add_q = "assignment_groupLIKEvita"

# Possível melhoria: configurável via settings
ADD_QUERY = settings.SERVICENOW_INCIDENT_FILTER
# "assignment_groupLIKEvita^ORassignment_groupLIKEvgr"
```

## Integração

### Dependências

- **ServiceNow API**: Endpoint `/api/now/table/incident`
- **Banco de Dados**: Tabela `incident`
- **Polars**: DataFrame processing
- **Django ORM**: Bulk operations

### Relacionamentos

- **Incident** ← dados extraídos
- **IncidentSla** ← relacionado por `task` (incident.sys_id)
- **IncidentTask** ← relacionado por `parent` (incident.sys_id)
- **Groups** ← referenciado por `assignment_group`

## Melhores Práticas

### Períodos Recomendados

```python
# ✅ Bom: Período diário
LoadIncidentsOpened("2025-01-20", "2025-01-20")

# ⚠️ Cuidado: Período semanal (volume alto)
LoadIncidentsOpened("2025-01-14", "2025-01-20") 

# ❌ Evitar: Período muito longo
LoadIncidentsOpened("2024-01-01", "2024-12-31")
```

### Horários de Execução

- **Recomendado**: Fora do horário comercial
- **Evitar**: Durante picos de uso do ServiceNow
- **Ideal**: Madrugada (2h-6h)

### Monitoramento

```python
# Alertas recomendados
if result['duration'] > 900:  # 15 minutos
    send_alert("LoadIncidentsOpened: Duração excessiva")
    
if result['n_inserted'] == 0:
    send_alert("LoadIncidentsOpened: Nenhum registro inserido")
    
if 'error' in result:
    send_alert(f"LoadIncidentsOpened: Erro - {result['error']}")
```

## Troubleshooting

### Problemas Frequentes

**1. Timeout de API**
```
Erro: requests.exceptions.ReadTimeout
Solução: Aumentar API_TIMEOUT ou reduzir período
```

**2. Dataset vazio**
```
Situação: n_inserted = 0
Possível causa: Filtro muito restritivo ou sem incidents no período
Verificação: Consultar ServiceNow manualmente
```

**3. Erro de schema**
```
Erro: polars.exceptions.SchemaError
Causa: ServiceNow retornou campo novo/removido
Solução: Atualizar modelo Incident
```

### Debug

```python
# Habilitar debug detalhado
import logging
logging.getLogger('api_service_now_new').setLevel(logging.DEBUG)

# Testar query manualmente
from api_service_now_new.utils.servicenow import paginate
result = paginate("incident", params={
    "sysparm_query": "opened_at>=2025-01-20 00:00:00",
    "sysparm_limit": "1"
})
print(f"Primeiro registro: {result[0] if result else 'Nenhum'}")
```

Esta task é fundamental para o pipeline de dados do ServiceNow e serve como base para análises de incidents e métricas de SLA.