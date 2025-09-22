# paginate()

## Visão Geral

A função `paginate()` é o coração da integração com APIs REST, especialmente ServiceNow. Ela gerencia automaticamente a paginação de grandes datasets, garantindo que todos os registros sejam extraídos sem limites de memória ou timeout.

## Assinatura

```python
def paginate(
    path: str,
    params: Optional[Dict] = None,
    limit: int = 10000,
    mode: str = "offset",
    limit_param: str = "sysparm_limit",
    offset_param: str = "sysparm_offset",
    cursor_param: str = "startingAfter",
    cursor_field: Optional[str] = None,
    result_key: str = "result",
) -> List[Dict]:
```

## Parâmetros Detalhados

### path (str)
**Obrigatório**. Endpoint da API relativo à base URL.

```python
# ✅ Correto
paginate("incident")                    # → /api/now/table/incident
paginate("sys_user")                    # → /api/now/table/sys_user
paginate("task_sla")                    # → /api/now/table/task_sla

# ❌ Evitar URLs completas
paginate("https://instance.service-now.com/api/now/table/incident")
```

### params (Optional[Dict])
Query parameters fixos aplicados a todas as páginas.

```python
# Filtros comuns
params = {
    "sysparm_query": "active=true^priority=1",
    "sysparm_fields": "sys_id,number,state,opened_at",
    "sysparm_exclude_reference_link": "true"
}

result = paginate("incident", params=params)
```

**Parâmetros ServiceNow Úteis**:
- `sysparm_query`: Filtros WHERE (encoded query)
- `sysparm_fields`: Campos a retornar (CSV)
- `sysparm_exclude_reference_link`: Remove links de referência
- `sysparm_display_value`: Retorna display values
- `sysparm_order_by`: Ordenação dos resultados

### limit (int)
Registros por página. **Padrão: 10000** (máximo ServiceNow).

```python
# ✅ Performance ótima (padrão)
paginate("incident", limit=10000)

# ⚠️ Mais páginas, mais requisições
paginate("incident", limit=1000)

# ❌ Pode causar timeout
paginate("incident", limit=50000)
```

### mode (str)
Tipo de paginação: `"offset"` ou `"cursor"`.

**Offset Mode (ServiceNow)**:
```python
paginate("incident", mode="offset", limit=10000)
# Page 1: ?sysparm_limit=10000&sysparm_offset=0
# Page 2: ?sysparm_limit=10000&sysparm_offset=10000  
# Page 3: ?sysparm_limit=10000&sysparm_offset=20000
```

**Cursor Mode (outras APIs)**:
```python
paginate("users", mode="cursor", cursor_field="id", cursor_param="after")
# Page 1: ?perPage=100
# Page 2: ?perPage=100&after=user123
# Page 3: ?perPage=100&after=user456
```

### limit_param / offset_param (str)
Nomes dos parâmetros para offset-based pagination.

```python
# ServiceNow (padrão)
paginate("incident", 
    limit_param="sysparm_limit", 
    offset_param="sysparm_offset"
)

# API personalizada
paginate("custom", 
    limit_param="page_size", 
    offset_param="page_offset"
)
```

### cursor_param / cursor_field (str)
Para cursor-based pagination.

```python
# API com cursor
paginate("items",
    mode="cursor",
    cursor_param="starting_after",  # Nome do parâmetro
    cursor_field="id"               # Campo do último registro
)
```

### result_key (str)
Chave do array de dados na resposta JSON. **Padrão: "result"**.

```python
# ServiceNow response structure
{
    "result": [
        {"sys_id": "abc", "number": "INC001"},
        {"sys_id": "def", "number": "INC002"}
    ]
}

# Outras APIs
{
    "data": [...],      # result_key="data"
    "items": [...],     # result_key="items"
    "records": [...]    # result_key="records"
}
```

## Algoritmo de Funcionamento

### Offset Mode (Padrão)

```python
all_results = []
offset = 0

while True:
    # 1. Constrói parâmetros da página
    page_params = {**params, limit_param: limit, offset_param: offset}
    
    # 2. Faz request
    response = requests.get(f"{base_url}/{path}", auth=auth, params=page_params)
    
    # 3. Extrai dados
    page_data = response.json().get(result_key, [])
    
    # 4. Verifica se acabaram os dados
    if not page_data:
        break
    
    # 5. Adiciona à lista total
    all_results.extend(page_data)
    
    # 6. Próxima página
    offset += limit
    print(offset)  # Progress indicator

return all_results
```

### Cursor Mode

```python
all_results = []
cursor = None

while True:
    # 1. Parâmetros com cursor (se existir)
    page_params = {**params, "perPage": limit}
    if cursor:
        page_params[cursor_param] = cursor
    
    # 2. Request
    response = requests.get(f"{base_url}/{path}", auth=auth, params=page_params)
    page_data = response.json().get(result_key, [])
    
    if not page_data:
        break
    
    all_results.extend(page_data)
    
    # 3. Próximo cursor
    if cursor_field:
        cursor = page_data[-1].get(cursor_field)
        if not cursor:
            break
    else:
        break  # Sem campo de cursor, não pode continuar

return all_results
```

## Processamento de Dados

### Normalização Automática

```python
# 1. Achatar referências ServiceNow
processed = []
for result in all_results:
    flat = flatten_reference_fields(dict(result))
    processed.append(flat)

# 2. Coletar todas as chaves possíveis
all_keys = set()
for record in processed:
    all_keys.update(record.keys())

# 3. Garantir chaves ETL
all_keys.update({"etl_created_at", "etl_updated_at"})

# 4. Normalizar cada registro
normalized = []
for record in processed:
    row = {}
    for key in all_keys:
        value = record.get(key)
        # Strings vazias → None
        if isinstance(value, str) and value.strip() == "":
            row[key] = None
        else:
            row[key] = str(value) if value is not None else None
    
    # Timestamps ETL
    now_iso = timezone.now().isoformat()
    row["etl_created_at"] = now_iso
    row["etl_updated_at"] = now_iso
    normalized.append(row)
```

### Exemplo de Transformação

**ServiceNow API Response**:
```json
{
  "result": [
    {
      "sys_id": "abc123",
      "number": "INC0001234",
      "assignment_group": {
        "value": "grp456",
        "display_value": "Vita Infrastructure"
      },
      "priority": "1",
      "description": ""
    }
  ]
}
```

**Após paginate()**:
```python
[
  {
    "sys_id": "abc123",
    "number": "INC0001234", 
    "assignment_group": "grp456",
    "dv_assignment_group": "Vita Infrastructure",
    "priority": "1",
    "description": None,  # String vazia → None
    "etl_created_at": "2025-01-20T10:15:30.123456Z",
    "etl_updated_at": "2025-01-20T10:15:30.123456Z"
  }
]
```

## Tratamento de Erros

### HTTP Errors

```python
if resp.status_code != 200:
    raise RuntimeError(f"API error: {resp.status_code} - {resp.text}")
```

**Códigos Comuns**:
- **401**: Credenciais inválidas
- **403**: Sem permissão para o endpoint
- **404**: Endpoint não existe
- **429**: Rate limit excedido
- **500**: Erro interno ServiceNow

### Network Errors

```python
try:
    result = paginate("incident", params={"sysparm_query": "priority=1"})
except requests.exceptions.Timeout:
    # Timeout da requisição
    logger.error("API timeout - considere reduzir page size")
except requests.exceptions.ConnectionError:
    # Erro de conectividade
    logger.error("Falha de conexão com ServiceNow")
except RuntimeError as e:
    # Erro HTTP (4xx, 5xx)
    logger.error(f"API retornou erro: {e}")
```

### Query Errors

```python
# ❌ Query inválida pode causar erro 400
bad_query = "priority=invalid_value"

# ✅ Validar queries antes de usar
valid_query = "priority=1^state=2"

try:
    result = paginate("incident", params={"sysparm_query": query})
except RuntimeError as e:
    if "400" in str(e):
        logger.error(f"Query inválida: {query}")
```

## Performance e Otimizações

### Métricas Típicas

| Dataset | Volume | Páginas | Tempo | Observações |
|---------|--------|---------|-------|-------------|
| **Incidents (dia)** | 1.000 | 1 | 5-15s | Volume baixo |
| **Incidents (mês)** | 25.000 | 3 | 30-90s | Volume médio |
| **SLAs (dia)** | 5.000 | 1 | 10-30s | Com dot-walk |
| **Users (todos)** | 50.000 | 5 | 5-15min | ❌ Evitar |

### Otimizações

**1. Page Size Máximo**
```python
# ✅ Use o máximo do ServiceNow
paginate("incident", limit=10000)

# ❌ Page size pequeno = mais requests
paginate("incident", limit=100)  # 100x mais requests!
```

**2. Filtros Restritivos**
```python
# ✅ Filtre o máximo possível
params = {
    "sysparm_query": "active=true^priority=1^opened_at>2025-01-01",
    "sysparm_fields": "sys_id,number,state"  # Apenas campos necessários
}

# ❌ Buscar tudo e filtrar localmente
params = {}  # Baixa dados desnecessários
```

**3. Campos Específicos**
```python
# ✅ Especifique campos necessários
fields = "sys_id,number,state,priority,opened_at"
params = {"sysparm_fields": fields}

# ❌ Retornar todos os campos
params = {}  # Inclui ~100 campos desnecessários
```

## Exemplos de Uso

### Incidents Básico

```python
from api_service_now_new.utils.servicenow import paginate

# Incidents de hoje
incidents = paginate(
    path="incident",
    params={
        "sysparm_query": "opened_at>=2025-01-20 00:00:00",
        "sysparm_fields": "sys_id,number,state,priority"
    }
)

print(f"Incidents encontrados: {len(incidents)}")
```

### SLAs com Dot-Walk

```python
# SLAs de incidents Vita
slas = paginate(
    path="task_sla",
    params={
        "sysparm_query": "taskISNOTEMPTY^task.assignment_group.nameLIKEvita",
        "sysparm_fields": "sys_id,task,sla,has_breached,percentage"
    }
)

print(f"SLAs Vita: {len(slas)}")
```

### Configurações (sem filtro temporal)

```python
# Todos os contratos SLA ativos
contracts = paginate(
    path="contract_sla", 
    params={
        "sysparm_query": "active=true",
        "sysparm_fields": "sys_id,name,duration"
    }
)

print(f"Contratos ativos: {len(contracts)}")
```

### Progress Tracking

```python
def paginate_with_progress(path, params=None, **kwargs):
    """Wrapper com progress tracking"""
    
    print(f"Iniciando paginação de {path}...")
    start_time = time.time()
    
    # Intercept print() calls from paginate
    original_print = print
    def progress_print(offset):
        elapsed = time.time() - start_time
        records_per_sec = offset / elapsed if elapsed > 0 else 0
        original_print(f"Processados: {offset:,} registros ({records_per_sec:.0f} rec/s)")
    
    # Temporariamente substitui print
    import builtins
    builtins.print = progress_print
    
    try:
        result = paginate(path, params, **kwargs)
        elapsed = time.time() - start_time
        original_print(f"✅ Concluído: {len(result):,} registros em {elapsed:.1f}s")
        return result
    finally:
        builtins.print = original_print
```

## Debug e Troubleshooting

### Testar Query

```python
# Testar query com limite pequeno
test_result = paginate("incident", params={
    "sysparm_query": "opened_at>=2025-01-20",
    "sysparm_limit": "1"  # Override limit
})

if test_result:
    print("✅ Query válida")
    print(f"Primeiro registro: {test_result[0]}")
else:
    print("❌ Query não retornou dados")
```

### Verificar Estrutura de Resposta

```python
import requests
from api_service_now_new.utils.servicenow import get_servicenow_env

base_url, auth, headers = get_servicenow_env()

# Request manual para debug
response = requests.get(
    f"{base_url}/incident",
    auth=auth,
    headers=headers,
    params={"sysparm_limit": "1"}
)

print(f"Status: {response.status_code}")
print(f"Response keys: {list(response.json().keys())}")
print(f"Result length: {len(response.json().get('result', []))}")
```

### Logging Detalhado

```python
import logging

# Ativar logs de requests
logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)

# Custom logging na paginate
def paginate_debug(path, params=None, **kwargs):
    logger = logging.getLogger(__name__)
    logger.info(f"Paginando {path} com params: {params}")
    
    result = paginate(path, params, **kwargs)
    
    logger.info(f"Resultado: {len(result)} registros")
    return result
```

Esta função é o alicerce de todas as integrações com ServiceNow e outras APIs REST, fornecendo paginação robusta e automática com tratamento de erros e normalização de dados.