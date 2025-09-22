# Utilitários

## Visão Geral

O módulo `utils` do `api_service_now_new` fornece funcionalidades de apoio para integração com a API do ServiceNow, incluindo autenticação, paginação, transformação de dados e operações de banco de dados.

## servicenow.py

### Funções de Ambiente

#### get_servicenow_env()

Obtém credenciais do ServiceNow via variáveis de ambiente.

```python
def get_servicenow_env() -> Tuple[str, tuple, Dict]:
    """
    Retorna (base_url, (user, password), headers) usando variáveis de ambiente.
    
    Variáveis necessárias:
    - SERVICE_NOW_BASE_URL
    - SERVICE_NOW_USERNAME  
    - SERVICE_NOW_USER_PASSWORD
    """
    base_url = os.getenv("SERVICE_NOW_BASE_URL")
    user = os.getenv("SERVICE_NOW_USERNAME")
    password = os.getenv("SERVICE_NOW_USER_PASSWORD")
    headers = {"Content-Type": "application/json"}
    
    if not all([base_url, user, password]):
        raise RuntimeError("Missing ServiceNow credentials in environment variables")
        
    return base_url, (user, password), headers
```

**Uso**:
```python
base_url, auth, headers = get_servicenow_env()
response = requests.get(f"{base_url}/api/now/table/incident", auth=auth, headers=headers)
```

### Paginação

#### paginate()

Função genérica para paginação de APIs REST com suporte a diferentes modos.

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

**Parâmetros**:

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `path` | str | Endpoint da API (ex: "incident") |
| `params` | Dict | Query parameters fixos |
| `limit` | int | Registros por página (padrão: 10000) |
| `mode` | str | "offset" ou "cursor" |
| `limit_param` | str | Nome do parâmetro de limite |
| `offset_param` | str | Nome do parâmetro de offset |
| `result_key` | str | Chave dos dados na resposta JSON |

**Modo Offset** (ServiceNow):
```python
incidents = paginate(
    path="incident",
    params={
        "sysparm_query": "opened_at>=2025-01-20 00:00:00",
        "sysparm_fields": "sys_id,number,state"
    },
    limit=10000,
    mode="offset"
)
```

**Características**:
- Paginação automática até esgotar dados
- Normalização de dados (strings vazias → None)
- Achatamento de campos de referência
- Adição de timestamps ETL

### Transformação de Dados

#### flatten_reference_fields()

Converte campos de referência do ServiceNow para valores simples.

```python
def flatten_reference_fields(data: dict) -> dict:
    """
    ServiceNow API retorna referências como:
    {"manager": {"value": "abc123", "display_value": "João Silva"}}
    
    Converte para:
    {"manager": "abc123", "dv_manager": "João Silva"}  
    """
    for key in list(data.keys()):
        value = data.get(key)
        if isinstance(value, dict) and "value" in value:
            data[key] = value.get("value")
            data[f"dv_{key}"] = value.get("display_value", "")
    return data
```

#### ensure_datetime()

Garante formato de datetime para filtros ServiceNow.

```python
def ensure_datetime(s: str, end: bool = False) -> str:
    """
    Completa timestamps para filtros ServiceNow.
    
    Input: "2025-01-20"
    Output: "2025-01-20 00:00:00" (start) ou "2025-01-20 23:59:59" (end)
    """
    if isinstance(s, str) and len(s) == 10:
        return f"{s} 23:59:59" if end else f"{s} 00:00:00"
    return s
```

### Operações de Banco

#### upsert_by_sys_id()

Operação upsert otimizada para modelos ServiceNow.

```python
@transaction.atomic
def upsert_by_sys_id(
    dataset: pl.DataFrame, 
    model, 
    log: Optional[Dict] = None
) -> None:
    """
    Upsert por sys_id preservando timestamps ETL.
    
    Estratégia:
    1. Identifica registros existentes por sys_id
    2. Separa em inserções (novos) e atualizações (existentes)  
    3. Executa bulk_create e bulk_update
    """
```

**Processo**:
1. **Validação**: Filtra apenas registros com sys_id válido
2. **Identificação**: Busca registros existentes no banco
3. **Separação**: Divide em `to_create` e `to_update`
4. **Execução**: Bulk operations com batch_size=1000
5. **Logging**: Atualiza contadores de inserção

**Exemplo**:
```python
# Carrega grupos do ServiceNow
result_list = paginate("sys_user_group", params={...})
dataset = pl.DataFrame(result_list)

# Upsert no banco
log = {"n_inserted": 0}
upsert_by_sys_id(dataset=dataset, model=Groups, log=log)
print(f"Inseridos: {log['n_inserted']} registros")
```

#### fetch_single_record()

Busca registro único por sys_id.

```python
def fetch_single_record(
    path: str, 
    sys_id: str, 
    params: Optional[Dict] = None, 
    timeout: int = 30
) -> Optional[Dict]:
    """
    Busca um único registro no ServiceNow por sys_id.
    
    Returns: Dict do registro ou None se não encontrado
    """
```

**Uso**:
```python
# Busca usuário específico
user = fetch_single_record("sys_user", "abc123def456")
if user:
    print(f"Usuário: {user['name']}")
else:
    print("Usuário não encontrado")
```

### Funções Depreciadas

Algumas funções são mantidas apenas para compatibilidade:

```python
def parse_datetime(value: str) -> Optional[datetime]:  # DEPRECIADO
def coerce_dates_in_dict(d: dict) -> dict:           # DEPRECIADO  
def normalize_date_columns(rows: List[Dict]) -> List[Dict]:  # DEPRECIADO
def process_data(data: List[Dict]) -> List[Dict]:     # Mantido para compatibilidade
```

## Padrões de Uso

### Extração Completa

```python
# 1. Configurar query
fields = ",".join([f.name for f in Model._meta.fields])
query = "active=true^nameSTARTSWITHVita"

# 2. Paginar dados
result_list = paginate(
    path="sys_user_group",
    params={
        "sysparm_fields": fields,
        "sysparm_query": query
    }
)

# 3. Transformar em DataFrame
dataset = pl.DataFrame(result_list, schema={f.name: pl.String for f in Model._meta.fields})

# 4. Carregar no banco
upsert_by_sys_id(dataset=dataset, model=Model, log=log)
```

### Extração com Filtro Temporal

```python
# 1. Preparar filtros de data
start_ts = ensure_datetime("2025-01-20", end=False)  # "2025-01-20 00:00:00"
end_ts = ensure_datetime("2025-01-20", end=True)     # "2025-01-20 23:59:59"

# 2. Construir query
query = f"opened_at>={start_ts}^opened_at<={end_ts}"

# 3. Extrair dados
result_list = paginate(
    path="incident",
    params={"sysparm_query": query, "sysparm_fields": fields}
)

# 4. Transformar e carregar
dataset = pl.DataFrame(result_list)
# Para incidents: usar delete+insert
with Pipeline() as pipeline:
    pipeline.load(dataset=dataset, model=Incident, filtro={"opened_at__gte": start_ts})
```

## Performance e Otimizações

### Configurações Recomendadas

```python
# Paginação otimizada para ServiceNow
SERVICENOW_PAGE_SIZE = 10000  # Máximo suportado
BATCH_SIZE = 1000            # Bulk operations
CONNECTION_TIMEOUT = 30      # Timeout API calls
```

### Monitoramento

```python
# Métricas por operação
metrics = {
    "api_requests": 0,
    "records_fetched": 0, 
    "records_inserted": 0,
    "records_updated": 0,
    "duration_seconds": 0
}

# Logging detalhado
logger.info(f"Fetched {len(result_list)} records in {duration}s")
logger.info(f"Inserted: {log['n_inserted']}, API calls: {api_calls}")
```

### Tratamento de Erros

```python
# API Errors
if resp.status_code != 200:
    raise RuntimeError(f"API error: {resp.status_code} - {resp.text}")

# Database Errors  
try:
    model.objects.bulk_update(to_update, update_fields, batch_size=1000)
except Exception:
    # Fallback para update individual
    for obj in to_update:
        try:
            obj.save(update_fields=update_fields)
        except Exception:
            logger.exception(f"Failed to update sys_id={obj.sys_id}")
```

## Configuração de Ambiente

### Variáveis Obrigatórias

```bash
# ServiceNow API
export SERVICE_NOW_BASE_URL="https://vitainstance.service-now.com/api/now/table"
export SERVICE_NOW_USERNAME="integration_user"
export SERVICE_NOW_USER_PASSWORD="secure_password"

# Database  
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# Logging
export LOG_LEVEL="INFO"
```

### Configuração Django

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'api_service_now_new.utils.servicenow': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'OPTIONS': {
                'MAX_CONNS': 20,
            }
        }
    }
}
```

## Extensibilidade

### Nova Função de Paginação

```python
def paginate_cursor_based(path: str, cursor_field: str, **kwargs):
    """Implementar paginação baseada em cursor para APIs que suportam"""
    pass

def paginate_with_retry(path: str, max_retries: int = 3, **kwargs):
    """Paginação com retry automático"""
    for attempt in range(max_retries):
        try:
            return paginate(path, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Backoff exponencial
```

### Novo Modo de Upsert

```python
def upsert_with_conflict_resolution(dataset, model, conflict_strategy="newest"):
    """
    Upsert com estratégias de resolução de conflito:
    - newest: Mantém registro mais recente
    - merge: Combina campos não-nulos
    - user_defined: Função customizada
    """
    pass
```

## Testes

### Casos de Teste Essenciais

```python
class TestServiceNowUtils(TestCase):
    def test_paginate_offset_mode(self):
        """Testa paginação com offset"""
        pass
        
    def test_flatten_reference_fields(self):
        """Testa achatamento de referências"""
        pass
        
    def test_upsert_by_sys_id(self):
        """Testa upsert com inserções e atualizações"""
        pass
        
    def test_error_handling(self):
        """Testa tratamento de erros de API"""
        pass
```

### Mocks Recomendados

```python
@patch('api_service_now_new.utils.servicenow.requests.get')
def test_paginate_api_error(self, mock_get):
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"
    
    with self.assertRaises(RuntimeError):
        paginate("incident", params={})
```

## Utilitários Detalhados

### Funções Principais
- [paginate()](paginate.md) - Paginação automática para APIs REST
- [upsert_by_sys_id()](upsert_by_sys_id.md) - Estratégia inteligente de INSERT/UPDATE
- [flatten_reference_fields()](flatten_reference_fields.md) - Converte referências ServiceNow
- [fetch_single_record()](fetch_single_record.md) - Busca registro individual por sys_id
- [get_servicenow_env()](get_servicenow_env.md) - Configuração de ambiente

### Funções de Apoio
- [ensure_datetime()](ensure_datetime.md) - Normalização de timestamps
- [process_data()](process_data.md) - Processamento legado de dados
```