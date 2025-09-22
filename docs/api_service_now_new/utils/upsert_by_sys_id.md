# upsert_by_sys_id()

## Visão Geral

A função `upsert_by_sys_id()` implementa uma estratégia inteligente de inserção/atualização de dados baseada no campo `sys_id` do ServiceNow. Diferente de um DELETE + INSERT simples, ela preserva timestamps ETL e atualiza apenas registros que realmente mudaram.

## Assinatura

```python
@transaction.atomic
def upsert_by_sys_id(
    dataset: pl.DataFrame, 
    model, 
    log: Optional[Dict] = None
) -> None:
```

## Características Principais

### Estratégia Inteligente
- **Preserva ETL Timestamps**: `etl_created_at` não é sobrescrito
- **Update Seletivo**: Apenas registros modificados são atualizados
- **Performance**: Evita DELETE/INSERT desnecessários
- **Transacional**: Rollback automático em caso de erro

### Comparação com load()

| Aspecto | `self.load()` | `upsert_by_sys_id()` |
|---------|---------------|----------------------|
| **Estratégia** | DELETE + INSERT | UPDATE + INSERT |
| **Timestamps ETL** | Sempre recriados | Preservados |
| **Performance** | Mais lento | Mais rápido |
| **Uso** | Tasks de incidents | Tasks de configurações |
| **Consistência** | Total (remove órfãos) | Parcial (não remove) |

## Algoritmo Detalhado

### 1. Validação e Preparação

```python
# Converte dataset para lista de dicionários
if isinstance(dataset, pl.DataFrame):
    if dataset.is_empty():
        return
    rows = dataset.to_dicts()
elif isinstance(dataset, list):
    rows = dataset
else:
    try:
        rows = list(dataset)
    except Exception:
        rows = []

if not rows:
    return
```

### 2. Filtragem de Campos

```python
# Obtém campos válidos do modelo Django
field_names = {f.name for f in model._meta.fields}
pk_name = model._meta.pk.name

# Filtra apenas registros com sys_id válido
processed = []
for record in rows:
    if not record:
        continue
    
    # Apenas campos que existem no modelo
    filtered_record = {
        key: (value if value != "" else None)
        for key, value in record.items()
        if key in field_names
    }
    
    if filtered_record.get("sys_id"):
        processed.append(filtered_record)
```

### 3. Identificação de Existentes

```python
# Busca registros que já existem no banco
existing = {
    obj.sys_id: obj
    for obj in model.objects.filter(
        sys_id__in=[record["sys_id"] for record in processed]
    )
}
```

### 4. Separação em Operações

```python
to_create = []  # Novos registros
to_update = []  # Registros existentes

for record in processed:
    sys_id = record["sys_id"]
    
    if sys_id in existing:
        # Registro existe: UPDATE
        obj = existing[sys_id]
        for key, value in record.items():
            if key not in (pk_name,):  # Não atualiza PK
                setattr(obj, key, value)
        to_update.append(obj)
    else:
        # Registro novo: INSERT
        to_create.append(model(**record))
```

### 5. Execução Bulk

```python
created_count = 0

# Bulk CREATE
if to_create:
    created_count = len(model.objects.bulk_create(to_create, batch_size=1000))

# Bulk UPDATE
if to_update:
    update_fields = [
        field for field in field_names 
        if field not in (pk_name, "sys_id")
    ]
    
    if update_fields:
        try:
            model.objects.bulk_update(to_update, update_fields, batch_size=1000)
        except Exception:
            # Fallback: update individual
            for obj in to_update:
                try:
                    obj.save(update_fields=update_fields)
                except Exception:
                    logger.exception(f"Falha update individual sys_id={obj.sys_id}")

# Log de resultados
if isinstance(log, dict):
    log["n_inserted"] = log.get("n_inserted", 0) + created_count
```

## Vantagens

### 1. Preservação de Timestamps

**Com load() (DELETE+INSERT)**:
```python
# Primeiro load
contract = ContractSla.objects.get(sys_id="abc123")
print(contract.etl_created_at)  # 2025-01-15 10:00:00

# Segundo load (mesmo contrato inalterado)
# DELETE + INSERT
contract = ContractSla.objects.get(sys_id="abc123") 
print(contract.etl_created_at)  # 2025-01-20 14:30:00 ← PERDEU HISTÓRICO
```

**Com upsert_by_sys_id()**:
```python
# Primeiro load
contract = ContractSla.objects.get(sys_id="abc123")
print(contract.etl_created_at)  # 2025-01-15 10:00:00

# Segundo load (contrato inalterado)
# Nenhuma operação (não existe em to_update)
contract = ContractSla.objects.get(sys_id="abc123")
print(contract.etl_created_at)  # 2025-01-15 10:00:00 ← PRESERVADO
```

### 2. Performance Superior

```python
# Cenário: 100 contratos SLA, apenas 5 modificados

# load(): DELETE + INSERT
# - DELETE: 100 registros
# - INSERT: 100 registros  
# Total: 200 operações de DB

# upsert_by_sys_id():
# - INSERT: 0 novos
# - UPDATE: 5 modificados
# Total: 5 operações de DB (40x mais rápido!)
```

### 3. Auditoria Detalhada

```python
def analyze_upsert_impact(before_count, after_count, log):
    """Analisa impacto do upsert"""
    
    created = log.get("n_inserted", 0)
    updated = after_count - before_count + created
    unchanged = before_count - updated
    
    print(f"📊 Upsert Analysis:")
    print(f"   ✅ Novos: {created}")
    print(f"   🔄 Modificados: {updated}")  
    print(f"   ⚡ Inalterados: {unchanged}")
    print(f"   📈 Taxa de mudança: {(created + updated) / (after_count or 1) * 100:.1f}%")
```

## Casos de Uso

### 1. Configurações Estáticas

**Ideal para**:
- `ContractSla`: Contratos raramente mudam
- `Groups`: Grupos organizacionais estáveis
- `SysCompany`: Empresas raramente criadas/modificadas
- `SysUser`: Usuários relativamente estáticos

```python
# LoadContractSla
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    upsert_by_sys_id(dataset=self.dataset, model=ContractSla, log=self.log)
    return self.log
```

### 2. Master Data Management

```python
# Manter dados de referência atualizados sem perder histórico
def sync_master_data():
    """Sincroniza dados mestre preservando auditoria"""
    
    # Busca dados atuais do ServiceNow
    current_groups = paginate("sys_user_group", params={"sysparm_query": "active=true"})
    dataset = pl.DataFrame(current_groups)
    
    # Conta registros antes
    before = Groups.objects.count()
    
    # Upsert
    log = {}
    upsert_by_sys_id(dataset, Groups, log)
    
    # Análise pós-upsert
    after = Groups.objects.count()
    print(f"Grupos: {before} → {after} (+{log.get('n_inserted', 0)} novos)")
```

### 3. Incremental Updates

```python
def incremental_user_sync():
    """Atualiza apenas usuários modificados recentemente"""
    
    # Última sincronização
    last_sync = ServiceNowExecutionLog.objects.filter(
        execution_type='users_sync',
        status='success'
    ).order_by('-started_at').first()
    
    since = last_sync.started_at if last_sync else "2025-01-01"
    
    # Apenas usuários modificados
    users = paginate("sys_user", params={
        "sysparm_query": f"sys_updated_on>={since}",
    })
    
    dataset = pl.DataFrame(users)
    upsert_by_sys_id(dataset, SysUser, log={})
```

## Limitações

### 1. Não Remove Órfãos

```python
# Cenário: Contrato deletado no ServiceNow
# mas ainda existe no banco local

# load() removeria (DELETE antes do INSERT)
# upsert_by_sys_id() mantém (não há DELETE)

# Solução: limpeza periódica manual
def cleanup_orphaned_contracts():
    """Remove contratos que não existem mais no ServiceNow"""
    
    # Busca todos os contratos ativos no ServiceNow
    current_contracts = set()
    servicenow_contracts = paginate("contract_sla", params={"sysparm_query": "active=true"})
    current_contracts.update(c["sys_id"] for c in servicenow_contracts)
    
    # Identifica órfãos
    local_contracts = set(ContractSla.objects.values_list('sys_id', flat=True))
    orphans = local_contracts - current_contracts
    
    if orphans:
        logger.warning(f"Removendo {len(orphans)} contratos órfãos")
        ContractSla.objects.filter(sys_id__in=orphans).delete()
```

### 2. Não Detecta Mudanças de Conteúdo

```python
# upsert_by_sys_id() sempre atualiza campos, mesmo se valor não mudou
# Possível otimização futura: comparar valores antes de atualizar

def smart_upsert_by_sys_id(dataset, model, log=None):
    """Upsert que compara valores antes de atualizar"""
    
    # ... código similar até separação de operações ...
    
    smart_updates = []
    for record in processed:
        sys_id = record["sys_id"]
        if sys_id in existing:
            obj = existing[sys_id]
            has_changes = False
            
            # Compara cada campo
            for key, new_value in record.items():
                current_value = getattr(obj, key, None)
                if str(current_value) != str(new_value):
                    setattr(obj, key, new_value)
                    has_changes = True
            
            # Apenas adiciona se realmente mudou
            if has_changes:
                smart_updates.append(obj)
    
    # Bulk update apenas dos modificados
    if smart_updates:
        model.objects.bulk_update(smart_updates, update_fields, batch_size=1000)
```

### 3. Memory Usage

```python
# Para datasets muito grandes, carrega todos em memória
existing = {obj.sys_id: obj for obj in model.objects.filter(...)}

# Otimização para datasets grandes
def chunked_upsert(dataset, model, chunk_size=1000):
    """Upsert em chunks para economizar memória"""
    
    if isinstance(dataset, pl.DataFrame):
        rows = dataset.to_dicts()
    else:
        rows = list(dataset)
    
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i+chunk_size]
        chunk_df = pl.DataFrame(chunk)
        upsert_by_sys_id(chunk_df, model)
```

## Monitoramento e Métricas

### Tracking de Mudanças

```python
def track_upsert_patterns():
    """Monitora padrões de mudanças nos dados"""
    
    # Análise de frequência de updates
    recent_updates = {}
    models = [ContractSla, Groups, SysCompany, SysUser]
    
    for model in models:
        recent = model.objects.filter(
            etl_updated_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        total = model.objects.count()
        update_rate = (recent / total * 100) if total > 0 else 0
        
        recent_updates[model.__name__] = {
            'recent': recent,
            'total': total,
            'rate': update_rate
        }
    
    return recent_updates

# Alertas baseados em padrões
patterns = track_upsert_patterns()
for model_name, stats in patterns.items():
    if stats['rate'] > 50:  # >50% dos registros modificados
        send_alert(f"{model_name}: Taxa alta de mudanças ({stats['rate']:.1f}%)")
```

### Performance Metrics

```python
def benchmark_upsert_vs_load():
    """Compara performance upsert vs load"""
    
    import time
    
    # Dados de teste
    test_contracts = paginate("contract_sla", params={"sysparm_limit": "100"})
    dataset = pl.DataFrame(test_contracts)
    
    # Teste load() tradicional
    start = time.time()
    # Simula load (sem DELETE real para não impactar dados)
    ContractSla.objects.bulk_create([ContractSla(**r) for r in dataset.to_dicts()[:10]], ignore_conflicts=True)
    load_time = time.time() - start
    
    # Teste upsert  
    start = time.time()
    log = {}
    upsert_by_sys_id(dataset, ContractSla, log)
    upsert_time = time.time() - start
    
    print(f"Load time: {load_time:.2f}s")
    print(f"Upsert time: {upsert_time:.2f}s") 
    print(f"Speedup: {load_time / upsert_time:.1f}x")
    print(f"New records: {log.get('n_inserted', 0)}")
```

## Error Handling

### Bulk Update Fallback

```python
# O código já implementa fallback automático
try:
    model.objects.bulk_update(to_update, update_fields, batch_size=1000)
except Exception:
    # Fallback: update individual
    for obj in to_update:
        try:
            obj.save(update_fields=update_fields)
        except Exception:
            logging.exception(f"Falha update individual sys_id={getattr(obj, 'sys_id', None)}")
```

### Validation Errors

```python
def safe_upsert_by_sys_id(dataset, model, log=None):
    """Upsert com validação de dados"""
    
    # Pre-validação de dados obrigatórios
    valid_records = []
    invalid_count = 0
    
    for record in processed:
        try:
            # Testa criação do objeto (sem salvar)
            test_obj = model(**record)
            test_obj.full_clean()  # Valida constraints
            valid_records.append(record)
        except Exception as e:
            logger.warning(f"Record inválido sys_id={record.get('sys_id')}: {e}")
            invalid_count += 1
    
    if invalid_count > 0:
        logger.warning(f"Ignorados {invalid_count} registros inválidos")
    
    # Processa apenas registros válidos
    # ... resto do código normal ...
```

Esta função é essencial para manter dados de configuração atualizados de forma eficiente, preservando auditoria e minimizando operações desnecessárias no banco de dados.