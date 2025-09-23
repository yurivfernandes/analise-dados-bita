# LoadIncidentTaskUpdated

## Visão Geral

A task `LoadIncidentTaskUpdated` realiza atualizações incrementais de incident tasks já existentes no banco de dados. Similar à `LoadIncidentSlaUpdated`, esta task atualiza apenas registros modificados, otimizando performance e preservando timestamps de auditoria ETL.

## Características

- **Tipo**: Task de Incidents (com período) - Modo UPDATE
- **Modelo**: `IncidentTask`
- **Filtro Principal**: `opened_at` (data de abertura da task)
- **Estratégia de Carga**: UPDATE (incremental)
- **Uso**: Atualizações durante o dia para tasks em andamento

## Implementação

### Classe Principal

```python
class LoadIncidentTaskUpdated(MixinGetDataset, Pipeline):
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()
```

### Diferenças da LoadIncidentTask

| Aspecto | LoadIncidentTask | LoadIncidentTaskUpdated |
|---------|-----------------|------------------------|
| **Estratégia** | DELETE + INSERT | UPDATE apenas |
| **Performance** | Mais lenta | Mais rápida |
| **Timestamps ETL** | Recria todos | Preserva `etl_created_at` |
| **Uso** | Carga inicial/diária | Atualizações incrementais |
| **Método `load()`** | Usa padrão Pipeline | Override personalizado |

### Query ServiceNow

```python
@property
def _incident_task(self) -> pl.DataFrame:
    start_ts = ensure_datetime(self.start_date, end=False)
    end_ts = ensure_datetime(self.end_date, end=True)

    fields = ",".join([
        f.name for f in IncidentTask._meta.fields
        if not f.name.startswith("etl_") and f.name != "etl_hash"
    ])

    query = f"opened_at>={start_ts} 00:00:00^opened_at<={end_ts} 23:59:59"
    add_q = "assignment_groupSTARTSWITHvita"
    if add_q not in query:
        query = f"{query}^{add_q}"

    params = {"sysparm_fields": fields, "sysparm_query": query}
    # ... paginação
```

**Filtros Idênticos à LoadIncidentTask**:
- `opened_at` no período especificado
- `assignment_groupSTARTSWITHvita` - Apenas tasks do grupo Vita

**Diferença da SLA Updated**: Usa `opened_at` ao invés de `sys_created_on`

## Estratégia UPDATE

### Método Load Personalizado

```python
def load(self, dataset: pl.DataFrame, model) -> None:
    self.log.setdefault("n_updated", 0)
    self._update(dataset=dataset, model=model)

@transaction.atomic
def _update(self, dataset: pl.DataFrame, model) -> None:
    if dataset.is_empty():
        self.log["n_updated"] = 0
        self.log.setdefault("update_duration", 0.0)
        return

    rows = dataset.to_dicts()
    sys_ids = [r.get("sys_id") for r in rows if r.get("sys_id")]
    if not sys_ids:
        self.log["n_updated"] = 0
        return

    # Buscar instâncias existentes em uma única query
    existing_qs = model.objects.filter(sys_id__in=sys_ids)
    existing_map = {getattr(obj, "sys_id"): obj for obj in existing_qs}

    # Campos atualizáveis (excluindo PK e campos auto-gerados)
    updatable_fields = [
        f.name for f in model._meta.fields
        if not getattr(f, "auto_created", False) and f.name != "sys_id"
    ]

    # Preparar atualizações
    instances_to_update = []
    for row in rows:
        sid = row.get("sys_id")
        inst = existing_map.get(sid)
        if not inst:
            continue  # Task não existe no banco, será ignorada
        
        # Aplicar mudanças à instância existente
        for k, v in row.items():
            if k in updatable_fields:
                setattr(inst, k, v)
        
        instances_to_update.append(inst)

    # Executar bulk_update com medição de tempo
    started = timezone.now()
    if instances_to_update:
        model.objects.bulk_update(
            instances_to_update, fields=updatable_fields, batch_size=1000
        )
    finished = timezone.now()
    
    duration = round((finished - started).total_seconds(), 2)
    self.log["n_updated"] = len(instances_to_update)
    self.log["update_duration"] = duration
```

### Performance Comparativa

| Métrica | LoadIncidentTask | LoadIncidentTaskUpdated |
|---------|-----------------|------------------------|
| **Volume Diário** | 800-3000 tasks | 800-3000 tasks |
| **Tempo Médio** | 3-6 minutos | 1-2 minutos |
| **I/O Banco** | Alto (DELETE+INSERT) | Médio (UPDATE) |
| **CPU** | Alto (re-indexação) | Baixo (updates localizados) |
| **Locks** | Table-level longos | Row-level curtos |

## Campos Tipicamente Atualizados

### Estados de Task que Mudam

```python
# Campos que frequentemente mudam durante o ciclo de vida da task
frequently_updated_fields = [
    'state',                    # 1=New, 2=In Progress, 3=Resolved, etc.
    'assigned_to',              # Reatribuição de responsável
    'work_notes',               # Adição de notas de trabalho
    'progress_notes',           # Notas de progresso
    'closed_at',                # Data de fechamento (quando resolvida)
    'resolved_at',              # Data de resolução
    'closure_code',             # Código de fechamento
    'close_notes',              # Notas de fechamento
    'actual_start_date',        # Início real do trabalho
    'actual_end_date',          # Fim real do trabalho
    'percent_complete',         # Percentual de conclusão
    'sys_updated_on',           # Timestamp de última modificação
    'sys_updated_by'            # Usuário que fez a última modificação
]

# Campos que raramente mudam após criação
rarely_updated_fields = [
    'number',                   # Número da task (imutável)
    'parent',                   # Incident pai (raramente muda)
    'opened_at',                # Data de abertura (imutável)
    'opened_by',                # Quem abriu (imutável)
    'short_description',        # Descrição (muda pouco)
    'assignment_group'          # Grupo (muda ocasionalmente)
]
```

## Casos de Uso

### 1. Atualização de Progresso

```python
def track_task_progress():
    """Acompanha progresso de tasks em andamento"""
    
    # Tasks abertas hoje que podem ter mudanças
    today = date.today().strftime("%Y-%m-%d")
    in_progress_tasks = IncidentTask.objects.filter(
        opened_at__date=today,
        state__in=['1', '2'],  # New, In Progress
        active='true'
    )
    
    if in_progress_tasks.count() > 50:  # Muitas tasks ativas
        logger.info(f"Tasks ativas detectadas: {in_progress_tasks.count()}")
        
        # Executa update para capturar mudanças
        result = LoadIncidentTaskUpdated(
            start_date=today,
            end_date=today
        ).run()
        
        # Verifica tasks que mudaram de estado
        recently_updated = IncidentTask.objects.filter(
            etl_updated_at__gte=timezone.now() - timedelta(minutes=30),
            sys_id__in=[t.sys_id for t in in_progress_tasks]
        )
        
        progress_summary = {
            'total_active': in_progress_tasks.count(),
            'recently_updated': recently_updated.count(),
            'update_result': result
        }
        
        return progress_summary
```

### 2. Monitoramento de Atribuições

```python
def monitor_task_assignments():
    """Monitora mudanças de atribuição em tasks"""
    
    # Tasks abertas nos últimos 3 dias (período de análise)
    cutoff_date = date.today() - timedelta(days=3)
    
    recent_tasks = IncidentTask.objects.filter(
        opened_at__date__gte=cutoff_date,
        state__in=['1', '2'],  # Ainda ativas
    )
    
    # Executa update para capturar reatribuições
    for single_date in [cutoff_date + timedelta(days=i) for i in range(4)]:
        date_str = single_date.strftime("%Y-%m-%d")
        LoadIncidentTaskUpdated(start_date=date_str, end_date=date_str).run()
    
    # Analisa mudanças de atribuição
    assignment_changes = []
    for task in recent_tasks:
        # Verificar se assigned_to mudou recentemente
        if task.etl_updated_at and task.etl_updated_at >= timezone.now() - timedelta(hours=2):
            assignment_changes.append({
                'task_number': task.number,
                'current_assignee': task.assigned_to,
                'assignment_group': task.assignment_group,
                'last_updated': task.etl_updated_at,
                'state': task.state
            })
    
    return {
        'total_monitored': recent_tasks.count(),
        'recent_changes': len(assignment_changes),
        'changes_detail': assignment_changes[:10]  # Top 10
    }
```

### 3. Detecção de Tasks Stale

```python
def detect_stale_tasks():
    """Detecta tasks que podem estar "travadas" """
    
    # Tasks em progresso há mais de 5 dias sem atualização
    stale_threshold = timezone.now() - timedelta(days=5)
    
    potentially_stale = IncidentTask.objects.filter(
        state='2',  # In Progress
        active='true',
        sys_updated_on__lt=stale_threshold  # ServiceNow timestamp antigo
    )
    
    if potentially_stale.exists():
        logger.warning(f"Tasks potencialmente travadas: {potentially_stale.count()}")
        
        # Força update para verificar se ainda são válidas
        date_range = []
        for task in potentially_stale:
            task_date = task.opened_at.date().strftime("%Y-%m-%d")
            if task_date not in date_range:
                date_range.append(task_date)
        
        # Update para cada data única
        for date_str in date_range:
            LoadIncidentTaskUpdated(start_date=date_str, end_date=date_str).run()
        
        # Re-verifica após update
        still_stale = IncidentTask.objects.filter(
            sys_id__in=[t.sys_id for t in potentially_stale],
            state='2',
            sys_updated_on__lt=stale_threshold
        )
        
        return {
            'initially_detected': potentially_stale.count(),
            'confirmed_stale': still_stale.count(),
            'resolved_by_update': potentially_stale.count() - still_stale.count(),
            'stale_tasks': [
                {'number': t.number, 'assigned_to': t.assigned_to, 'days_stale': (timezone.now() - t.sys_updated_on).days}
                for t in still_stale[:5]
            ]
        }
    
    return {'message': 'Nenhuma task stale detectada'}
```

## Integração com Workflow

### Pipeline de Atualização

```python
def integrated_task_update_pipeline(target_date):
    """Pipeline integrado de atualização de tasks"""
    
    date_str = target_date.strftime("%Y-%m-%d")
    pipeline_result = {
        'date': date_str,
        'stages': {}
    }
    
    # Stage 1: Update incremental
    logger.info("Stage 1: Executando update incremental de tasks")
    update_result = LoadIncidentTaskUpdated(
        start_date=date_str, 
        end_date=date_str
    ).run()
    
    pipeline_result['stages']['incremental_update'] = update_result
    
    # Stage 2: Análise de mudanças
    logger.info("Stage 2: Analisando mudanças detectadas")
    if update_result.get('n_updated', 0) > 0:
        changes_analysis = analyze_task_changes(target_date)
        pipeline_result['stages']['changes_analysis'] = changes_analysis
    
    # Stage 3: Validação de integridade
    logger.info("Stage 3: Validando integridade dos dados")
    integrity_check = validate_task_integrity(target_date)
    pipeline_result['stages']['integrity_check'] = integrity_check
    
    # Stage 4: Alertas e notificações
    if integrity_check.get('issues_found', 0) > 0:
        logger.warning("Stage 4: Issues detectados, enviando alertas")
        alerts = send_task_update_alerts(integrity_check['issues'])
        pipeline_result['stages']['alerts'] = alerts
    
    return pipeline_result

def analyze_task_changes(target_date):
    """Analisa tipos de mudanças em tasks"""
    
    recent_updates = IncidentTask.objects.filter(
        etl_updated_at__date=target_date
    )
    
    changes_by_type = {
        'state_changes': recent_updates.filter(
            state__in=['3', '7']  # Resolved, Closed
        ).count(),
        'assignment_changes': 0,  # Seria necessário histórico
        'notes_updates': recent_updates.exclude(
            work_notes__isnull=True
        ).exclude(work_notes='').count(),
        'total_updated': recent_updates.count()
    }
    
    return changes_by_type

def validate_task_integrity(target_date):
    """Valida integridade das tasks atualizadas"""
    
    tasks_today = IncidentTask.objects.filter(
        Q(opened_at__date=target_date) | Q(etl_updated_at__date=target_date)
    )
    
    issues = []
    
    # 1. Tasks órfãs (parent incident inexistente)
    orphaned_tasks = tasks_today.extra(
        where=["parent NOT IN (SELECT sys_id FROM incident WHERE sys_id IS NOT NULL)"]
    ).filter(parent__isnull=False).exclude(parent='')
    
    if orphaned_tasks.exists():
        issues.append(f"Tasks órfãs: {orphaned_tasks.count()}")
    
    # 2. Tasks fechadas sem closure_code
    closed_without_code = tasks_today.filter(
        state__in=['3', '7'],  # Resolved/Closed
        closure_code__isnull=True
    )
    
    if closed_without_code.exists():
        issues.append(f"Tasks fechadas sem código: {closed_without_code.count()}")
    
    # 3. Tasks com timestamps inconsistentes
    time_inconsistencies = tasks_today.filter(
        closed_at__isnull=False,
        resolved_at__isnull=False,
        closed_at__lt=F('resolved_at')
    )
    
    if time_inconsistencies.exists():
        issues.append(f"Timestamps inconsistentes: {time_inconsistencies.count()}")
    
    return {
        'validation_date': target_date,
        'total_tasks_checked': tasks_today.count(),
        'issues_found': len(issues),
        'issues': issues
    }
```

## Monitoramento Específico

### Métricas de Update

```python
def task_update_metrics():
    """Métricas específicas de updates de tasks"""
    
    today = date.today()
    
    # Tasks que mudaram hoje
    updated_today = IncidentTask.objects.filter(
        etl_updated_at__date=today
    )
    
    # Distribuição por tipo de mudança
    state_transitions = {}
    for task in updated_today:
        state_transitions.setdefault(task.state, 0)
        state_transitions[task.state] += 1
    
    # Performance de resolução
    resolved_today = updated_today.filter(state='3')  # Resolved
    
    resolution_stats = {
        'total_resolved': resolved_today.count(),
        'avg_resolution_time': None,
        'resolution_by_group': {}
    }
    
    if resolved_today.exists():
        # Calcular tempo médio de resolução
        resolution_times = []
        for task in resolved_today:
            if task.opened_at and task.resolved_at:
                duration = (task.resolved_at - task.opened_at).total_seconds() / 3600
                resolution_times.append(duration)
        
        if resolution_times:
            resolution_stats['avg_resolution_time'] = round(
                sum(resolution_times) / len(resolution_times), 2
            )
        
        # Por grupo de atribuição
        for task in resolved_today:
            group = task.assignment_group or 'Unassigned'
            resolution_stats['resolution_by_group'].setdefault(group, 0)
            resolution_stats['resolution_by_group'][group] += 1
    
    return {
        'update_summary': {
            'total_updated': updated_today.count(),
            'state_distribution': state_transitions,
            'update_percentage': round(
                (updated_today.count() / IncidentTask.objects.filter(
                    opened_at__date=today
                ).count()) * 100, 1
            ) if IncidentTask.objects.filter(opened_at__date=today).exists() else 0
        },
        'resolution_stats': resolution_stats
    }
```

### Alertas de Update

```python
def task_update_alerts():
    """Alertas específicos para updates de tasks"""
    
    alerts = []
    today = date.today()
    
    # 1. Baixa taxa de atualização
    tasks_today = IncidentTask.objects.filter(opened_at__date=today)
    updated_today = IncidentTask.objects.filter(etl_updated_at__date=today)
    
    if tasks_today.exists():
        update_rate = updated_today.count() / tasks_today.count()
        if update_rate < 0.05:  # < 5% das tasks foram atualizadas
            alerts.append({
                'type': 'low_update_rate',
                'message': f'Taxa baixa de atualização: {update_rate:.1%}',
                'severity': 'warning'
            })
    
    # 2. Tasks travadas há muito tempo
    stale_tasks = IncidentTask.objects.filter(
        state='2',  # In Progress
        active='true',
        sys_updated_on__lt=timezone.now() - timedelta(days=7)
    )
    
    if stale_tasks.count() > 10:
        alerts.append({
            'type': 'stale_tasks',
            'message': f'{stale_tasks.count()} tasks sem atualização há 7+ dias',
            'severity': 'warning'
        })
    
    # 3. Muitas tasks órfãs detectadas
    orphaned_count = IncidentTask.objects.extra(
        where=["parent NOT IN (SELECT sys_id FROM incident WHERE sys_id IS NOT NULL)"]
    ).filter(
        etl_updated_at__date=today
    ).count()
    
    if orphaned_count > 5:
        alerts.append({
            'type': 'orphaned_tasks',
            'message': f'{orphaned_count} tasks órfãs detectadas',
            'severity': 'error'
        })
    
    # 4. Pico de atualizações (pode indicar problema)
    if updated_today.count() > tasks_today.count() * 2:  # Mais de 200% de updates
        alerts.append({
            'type': 'update_spike',
            'message': f'Pico anormal de atualizações: {updated_today.count()}',
            'severity': 'info'
        })
    
    return alerts
```

Esta task é fundamental para manter o estado atual das incident tasks atualizado durante o dia, permitindo acompanhamento em tempo real do progresso na resolução de incidents.