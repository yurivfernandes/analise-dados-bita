# LoadAstContract

## Descrição

A task `LoadAstContract` é responsável por extrair, transformar e carregar dados da tabela `ast_contract` do ServiceNow para o banco de dados local. Esta task faz parte do conjunto de tasks de configuração do ServiceNow e carrega contratos de ativos.

## Funcionalidades

### Extração de Dados
- Extrai dados da tabela `ast_contract` do ServiceNow via API REST
- Utiliza paginação otimizada com limite de 10.000 registros por página
- Aplica filtros específicos para empresas relevantes

### Filtros Aplicados
- **Empresas filtradas por nome**:
  - Contratos que começam com "vita"
  - Contratos que começam com "vgr" 
  - Contratos que começam com "bradesco"
- **Query ServiceNow**: `nameSTARTSWITHvita^ORnameSTARTSWITHvgr^ORnameSTARTSWITHbradesco`

### Campos Extraídos
Todos os campos da tabela `ast_contract`, incluindo:

**Campos básicos:**
- `sys_id`, `sys_created_on`, `sys_updated_on`
- `number`, `active`, `state`, `description`

**Informações contratuais:**
- `starts`, `ends`, `renewal_date`, `renewal_end_date`
- `vendor`, `contract_administrator`, `business_owner`
- `payment_amount`, `total_cost`, `monthly_cost`, `yearly_cost`

**Campos de relacionamento:**
- Todos os campos `dv_*` (display values) para referências

**Campos customizados:**
- `u_*` (campos específicos da implementação)

### Transformação
- Converte todos os campos para string (pl.String)
- Mantém estrutura original dos dados do ServiceNow
- Não aplica transformações específicas de negócio

### Carregamento
- Utiliza estratégia de `upsert_by_sys_id`
- Insere novos registros e atualiza existentes baseado no `sys_id`
- Modelo de destino: `AstContract`

## Configuração

### Herança
```python
class LoadAstContract(MixinGetDataset, Pipeline)
```

### Parâmetros de Paginação
- **Limite por página**: 10.000 registros
- **Modo**: offset
- **Parâmetros**: `sysparm_limit`, `sysparm_offset`

## Execução

### Síncrona
```python
from api_service_now_new.tasks import LoadAstContract

task = LoadAstContract()
result = task.run()
```

### Assíncrona (Celery)
```python
from api_service_now_new.tasks import load_ast_contract_async

result = load_ast_contract_async.delay()
```

### Via API (LoadConfigurationsView)
A task é executada automaticamente como parte do conjunto de configurações:
```bash
POST /api/service-now-new/load-configurations/
```

## Configuração de Retry

- **Tentativas máximas**: 3
- **Backoff**: 5 segundos
- **Retry automático**: Em caso de Exception

## Log de Execução

A task retorna um dicionário com informações de execução:
- Número de registros processados
- Tempo de execução
- Status da operação
- Eventuais erros ou warnings

## Dependências

- **ServiceNow API**: Acesso à tabela `ast_contract`
- **Banco de dados**: Tabela `ast_contract` criada
- **Modelo Django**: `AstContract`

## Relacionamento com Outras Tasks

Faz parte do grupo de **tasks de configuração**, executadas em paralelo:
- `LoadContractSla`
- `LoadGroups`
- `LoadSysCompany`
- `LoadSysUser`
- `LoadCmdbCiNetworkLink`
- **`LoadAstContract`** (nova)

## Modelo de Dados

Tabela de destino: `ast_contract`
- **Primary Key**: `sys_id`
- **Campos**: 89+ campos incluindo display values
- **Tipo de dados**: Todos os campos são TextField
- **Collation**: SQL_Latin1_General_CP1_CI_AS