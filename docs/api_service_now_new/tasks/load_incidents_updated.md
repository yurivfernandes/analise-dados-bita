# LoadIncidentsUpdated

## Visão Geral

A task `LoadIncidentsUpdated` realiza atualizações incrementais de incidents já existentes no banco de dados. Diferentemente da `LoadIncidentsOpened` que filtra por `opened_at` e faz DELETE+INSERT, esta task filtra por `sys_updated_on` e executa apenas UPDATEs, capturando mudanças em incidents que já existem no sistema.

## Características

- **Tipo**: Task de Incidents (com período) - Modo UPDATE
- **Modelo**: `Incident`
- **Filtro Principal**: `sys_updated_on` (data de última modificação)
- **Estratégia de Carga**: UPDATE (incremental)
- **Uso**: Atualizações durante o dia para incidents em andamento

## Implementação

### Classe Principal

```python
class LoadIncidentsUpdated(MixinGetDataset, Pipeline):
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()
```

### Diferenças Fundamentais

| Aspecto | LoadIncidentsOpened | LoadIncidentsUpdated |
|---------|-------------------|---------------------|
| **Filtro Temporal** | `opened_at` | `sys_updated_on` |
| **Propósito** | Incidents novos | Incidents modificados |
| **Estratégia** | DELETE + INSERT | UPDATE apenas |
| **Performance** | Mais lenta | Mais rápida |
| **Timestamps ETL** | Recria todos | Preserva `etl_created_at` |
| **Volume Típico** | 500-2000/dia | 200-1000/dia |

### Query ServiceNow Específica

```python
@property
def _incidents(self) -> pl.DataFrame:
    start_ts = ensure_datetime(self.start_date, end=False)
    end_ts = ensure_datetime(self.end_date, end=True)

    # Campos idênticos à LoadIncidentsOpened
    fields = ",".join([
        f.name for f in Incident._meta.fields 
        if not f.name.startswith("etl_") and f.name != "etl_hash"
    ])

    # Filtro principal: sys_updated_on (não opened_at)
    query = f"sys_updated_on>={start_ts}^sys_updated_on<={end_ts}^assignment_groupSTARTSWITHvita"
    
    params = {"sysparm_query": query, "sysparm_fields": fields}
    
    result_list = paginate(
        path="incident",
        params=params,
        limit=10000,
        mode="offset",
        limit_param="sysparm_limit",
        offset_param="sysparm_offset",
        result_key="result",
    )
    
    return pl.DataFrame(
        result_list,
        schema={f.name: pl.String for f in Incident._meta.fields},
    )
```

**Diferenças na Query**:
- `sys_updated_on>=2025-01-20 00:00:00` ao invés de `opened_at>=...`
- Captura incidents modificados no período, independente de quando foram criados
- Mesmo filtro de grupo: `assignment_groupSTARTSWITHvita`

## Estratégia UPDATE

### Implementação de Update Personalizada

```python
def load(self, dataset: pl.DataFrame, model) -> None:
    """Override: não faz delete+insert; apenas faz update dos registros por `sys_id`."""
    self.log.setdefault("n_updated", 0)
    self._update(dataset=dataset, model=model)

@transaction.atomic
def _update(self, dataset: pl.DataFrame, model) -> None:
    """Atualiza registros existentes por `sys_id` usando bulk_update.
    
    Estratégia:
    - Extrair sys_ids do dataset
    - Buscar as instâncias existentes em um único query
    - Atualizar atributos em memória e usar `bulk_update`
    """
    if dataset.is_empty():
        self.log["n_updated"] = 0
        self.log.setdefault("update_duration", 0.0)
        return

    rows = dataset.to_dicts()
    sys_ids = [r.get("sys_id") for r in rows if r.get("sys_id")]
    if not sys_ids:
        self.log["n_updated"] = 0
        return

    # Buscar instâncias existentes
    existing_qs = model.objects.filter(sys_id__in=sys_ids)
    existing_map = {getattr(obj, "sys_id"): obj for obj in existing_qs}

    # Campos do model a serem atualizados (exclui pk e sys_id)
    updatable_fields = [
        f.name for f in model._meta.fields
        if not getattr(f, "auto_created", False) and f.name != "sys_id"
    ]

    instances_to_update = []
    for row in rows:
        sid = row.get("sys_id")
        inst = existing_map.get(sid)
        if not inst:
            continue  # Incident não existe no banco, será ignorado
        
        for k, v in row.items():
            if k in updatable_fields:
                setattr(inst, k, v)
        instances_to_update.append(inst)

    # Executar bulk_update com medição de performance
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

### Vantagens da Estratégia UPDATE

**1. Performance Superior**
```python
# LoadIncidentsOpened (DELETE+INSERT)
# - Deleta: 1500 incidents (5-10s)
# - Insere: 1500 incidents (30-60s) 
# - Total: 35-70 segundos

# LoadIncidentsUpdated (UPDATE)
# - Atualiza: 800 incidents (10-20s)
# - Total: 10-20 segundos
```

**2. Preservação de Histórico ETL**
```python
# Antes do update
incident.etl_created_at = "2025-01-20 08:00:00"  # Preservado
incident.etl_updated_at = "2025-01-20 08:00:00"

# Após update
incident.etl_created_at = "2025-01-20 08:00:00"  # ✅ Mantido
incident.etl_updated_at = "2025-01-20 14:30:00"  # ✅ Atualizado
```

**3. Menor Impacto no Sistema**
- Sem interrupção na disponibilidade dos dados
- Não recria índices e constraints
- Transações mais leves

## Campos Frequentemente Atualizados

### Estados do Incident que Mudam

```python
# Campos que frequentemente mudam durante lifecycle do incident
frequently_updated_fields = [
    'incident_state',           # 1=New, 2=In Progress, 6=Resolved, 7=Closed
    'state',                    # Estado geral da task
    'assigned_to',              # Reatribuição de responsável
    'assignment_group',         # Mudança de grupo (escalation)
    'work_notes',               # Adição de notas de trabalho
    'comments',                 # Comentários adicionais
    'resolved_at',              # Data de resolução
    'closed_at',                # Data de fechamento
    'resolution_code',          # Código de resolução
    'close_code',               # Código de fechamento
    'close_notes',              # Notas de fechamento
    'priority',                 # Mudança de prioridade
    'urgency',                  # Mudança de urgência
    'impact',                   # Mudança de impacto
    'escalation',               # Nível de escalation
    'hold_reason',              # Razão de hold/pause
    'sys_updated_on',           # Timestamp de modificação
    'sys_updated_by',           # Usuário que modificou
    'u_resolution_time',        # Tempo de resolução calculado
    'u_response_time'           # Tempo de primeira resposta
]

# Campos que raramente mudam após criação
rarely_updated_fields = [
    'number',                   # Número do incident (imutável)
    'opened_at',                # Data de abertura (imutável) 
    'opened_by',                # Quem abriu (imutável)
    'caller_id',                # Solicitante (raramente muda)
    'location',                 # Localização (raramente muda)
    'category',                 # Categoria (ocasional)
    'subcategory',              # Subcategoria (ocasional)
    'u_affected_ci'             # CI afetado (ocasional)
]
```

## Casos de Uso Específicos

### 1. Acompanhamento de Resolução

```python
def track_resolution_progress():
    """Acompanha progresso na resolução de incidents"""
    
    # Incidents abertos nos últimos 7 dias (ainda podem ser atualizados)
    active_period_start = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    
    # Buscar incidents ativos que podem ter mudanças
    active_incidents = Incident.objects.filter(
        opened_at__date__gte=active_period_start,
        incident_state__in=['1', '2', '3'],  # New, In Progress, On Hold
    )
    
    if active_incidents.count() > 100:  # Threshold para executar update
        logger.info(f"Incidents ativos detectados: {active_incidents.count()}")
        
        # Executa update para capturar mudanças
        result = LoadIncidentsUpdated(
            start_date=today,
            end_date=today
        ).run()
        
        # Analisa mudanças capturadas
        recently_resolved = Incident.objects.filter(
            etl_updated_at__gte=timezone.now() - timedelta(minutes=30),
            incident_state='6'  # Resolved
        )
        
        recently_closed = Incident.objects.filter(
            etl_updated_at__gte=timezone.now() - timedelta(minutes=30),
            incident_state='7'  # Closed
        )
        
        return {
            'total_active': active_incidents.count(),
            'recently_resolved': recently_resolved.count(),
            'recently_closed': recently_closed.count(),
            'update_result': result
        }
```

### 2. Detecção de Escalations

```python
def detect_escalations():
    """Detecta incidents que foram escalados"""
    
    today = date.today().strftime("%Y-%m-%d")
    
    # Executa update para capturar mudanças recentes
    LoadIncidentsUpdated(start_date=today, end_date=today).run()
    
    # Incidents atualizados recentemente
    recently_updated = Incident.objects.filter(
        etl_updated_at__gte=timezone.now() - timedelta(hours=2)
    )
    
    escalation_indicators = []
    for incident in recently_updated:
        escalation_score = 0
        reasons = []
        
        # 1. Mudança de prioridade para alta
        if incident.priority == '1':  # Critical
            escalation_score += 3
            reasons.append('Critical priority')
        elif incident.priority == '2':  # High
            escalation_score += 2
            reasons.append('High priority')
        
        # 2. Campo escalation preenchido
        if incident.escalation and incident.escalation != '0':
            escalation_score += 2
            reasons.append(f'Escalation level: {incident.escalation}')
        
        # 3. Mudança de grupo (pode indicar escalation)
        # (necessário comparar com valor anterior - seria necessário histórico)
        
        # 4. Urgência alta
        if incident.urgency == '1':  # High urgency
            escalation_score += 1
            reasons.append('High urgency')
        
        if escalation_score >= 2:  # Threshold para considerar escalation
            escalation_indicators.append({
                'incident_number': incident.number,
                'escalation_score': escalation_score,
                'reasons': reasons,
                'current_state': incident.incident_state,
                'assigned_to': incident.assigned_to,
                'assignment_group': incident.assignment_group,
                'last_updated': incident.etl_updated_at.isoformat()
            })
    
    return {
        'total_updated': recently_updated.count(),
        'escalated_detected': len(escalation_indicators),
        'escalations': escalation_indicators
    }
```

### 3. Monitoramento de SLA Risk

```python
def monitor_sla_risk():
    """Monitora incidents em risco de breach de SLA"""
    
    # Executa update para dados atuais
    today = date.today().strftime("%Y-%m-%d")
    LoadIncidentsUpdated(start_date=today, end_date=today).run()
    
    # Incidents abertos há mais tempo (risco de SLA breach)
    sla_risk_threshold = timezone.now() - timedelta(hours=4)  # 4h+ abertos
    
    at_risk_incidents = Incident.objects.filter(
        incident_state__in=['1', '2'],  # New, In Progress
        opened_at__lt=sla_risk_threshold,
        priority__in=['1', '2']  # High priority incidents
    )
    
    risk_analysis = []
    for incident in at_risk_incidents:
        # Calcular tempo aberto
        time_open = timezone.now() - incident.opened_at
        hours_open = time_open.total_seconds() / 3600
        
        # Determinar nível de risco baseado em prioridade e tempo
        if incident.priority == '1':  # Critical
            if hours_open > 4:
                risk_level = 'CRITICAL'
            elif hours_open > 2:
                risk_level = 'HIGH'
            else:
                risk_level = 'MEDIUM'
        elif incident.priority == '2':  # High
            if hours_open > 8:
                risk_level = 'HIGH'
            elif hours_open > 4:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
        else:
            risk_level = 'LOW'
        
        risk_analysis.append({
            'incident_number': incident.number,
            'priority': incident.priority,
            'hours_open': round(hours_open, 1),
            'risk_level': risk_level,
            'assigned_to': incident.assigned_to,
            'assignment_group': incident.assignment_group,
            'short_description': incident.short_description[:100] + '...' if len(incident.short_description or '') > 100 else incident.short_description
        })
    
    # Ordenar por risco e tempo
    risk_analysis.sort(key=lambda x: (
        {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}[x['risk_level']],
        -x['hours_open']
    ), reverse=True)
    
    return {
        'total_at_risk': len(risk_analysis),
        'by_risk_level': {
            'CRITICAL': len([r for r in risk_analysis if r['risk_level'] == 'CRITICAL']),
            'HIGH': len([r for r in risk_analysis if r['risk_level'] == 'HIGH']),
            'MEDIUM': len([r for r in risk_analysis if r['risk_level'] == 'MEDIUM']),
            'LOW': len([r for r in risk_analysis if r['risk_level'] == 'LOW']),
        },
        'top_risks': risk_analysis[:10]
    }
```

## Performance e Monitoramento

### Métricas de Update

```python
def incidents_update_metrics():
    """Métricas específicas de updates de incidents"""
    
    today = date.today()
    
    # Incidents atualizados hoje
    updated_today = Incident.objects.filter(
        etl_updated_at__date=today
    )
    
    # Incidents abertos hoje (para comparação)
    opened_today = Incident.objects.filter(
        opened_at__date=today
    )
    
    # Análise de tipos de mudança
    state_changes = {}
    priority_changes = {}
    
    for incident in updated_today:
        # Distribuição por estado atual
        state_changes.setdefault(incident.incident_state, 0)
        state_changes[incident.incident_state] += 1
        
        # Distribuição por prioridade
        priority_changes.setdefault(incident.priority, 0)
        priority_changes[incident.priority] += 1
    
    # Incidents resolvidos hoje
    resolved_today = updated_today.filter(incident_state='6')
    closed_today = updated_today.filter(incident_state='7')
    
    return {
        'update_overview': {
            'total_updated': updated_today.count(),
            'total_opened_today': opened_today.count(),
            'update_ratio': round(
                (updated_today.count() / max(opened_today.count(), 1)) * 100, 1
            )
        },
        'state_distribution': state_changes,
        'priority_distribution': priority_changes,
        'resolution_stats': {
            'resolved_today': resolved_today.count(),
            'closed_today': closed_today.count(),
            'total_completed': resolved_today.count() + closed_today.count()
        }
    }
```

### Alertas Específicos

```python
def incidents_update_alerts():
    """Alertas específicos para updates de incidents"""
    
    alerts = []
    today = date.today()
    
    # 1. Muitos incidents críticos atualizados (pode indicar problema sistêmico)
    critical_updates = Incident.objects.filter(
        etl_updated_at__date=today,
        priority='1'  # Critical
    ).count()
    
    if critical_updates > 20:  # Threshold ajustável
        alerts.append({
            'type': 'critical_incidents_spike',
            'message': f'{critical_updates} incidents críticos atualizados hoje',
            'severity': 'high'
        })
    
    # 2. Taxa de update muito baixa (pode indicar problema na API)
    opened_today = Incident.objects.filter(opened_at__date=today).count()
    updated_today = Incident.objects.filter(etl_updated_at__date=today).count()
    
    if opened_today > 0:
        update_rate = updated_today / opened_today
        if update_rate < 0.1:  # Menos de 10% de update rate
            alerts.append({
                'type': 'low_update_rate',
                'message': f'Taxa de update baixa: {update_rate:.1%} ({updated_today}/{opened_today})',
                'severity': 'warning'
            })
    
    # 3. Incidents antigos sendo atualizados (pode indicar descoberta de problemas)
    old_incidents_updated = Incident.objects.filter(
        etl_updated_at__date=today,
        opened_at__date__lt=today - timedelta(days=30)  # Abertos há mais de 30 dias
    ).count()
    
    if old_incidents_updated > 10:
        alerts.append({
            'type': 'old_incidents_updated',
            'message': f'{old_incidents_updated} incidents antigos (30+ dias) foram atualizados',
            'severity': 'info'
        })
    
    # 4. Pico de escalations
    escalated_today = Incident.objects.filter(
        etl_updated_at__date=today,
        escalation__isnull=False
    ).exclude(escalation='0').count()
    
    if escalated_today > 15:  # Threshold para escalations
        alerts.append({
            'type': 'escalation_spike',
            'message': f'Pico de escalations detectado: {escalated_today} incidents',
            'severity': 'warning'
        })
    
    return alerts
```

## Integração com LoadIncidentsOpened

### Estratégia Combinada

```python
def combined_incidents_strategy(target_date):
    """Estratégia combinada: abertura + atualizações"""
    
    date_str = target_date.strftime("%Y-%m-%d")
    
    # Horário da execução determina estratégia
    current_hour = timezone.now().hour
    
    if current_hour < 6:  # Madrugada: carga completa
        logger.info("Executando carga completa de incidents")
        
        # 1. Incidents novos
        opened_result = LoadIncidentsOpened(
            start_date=date_str, 
            end_date=date_str
        ).run()
        
        # 2. Updates de incidents existentes
        updated_result = LoadIncidentsUpdated(
            start_date=date_str, 
            end_date=date_str
        ).run()
        
        return {
            'strategy': 'full_load',
            'opened_incidents': opened_result,
            'updated_incidents': updated_result,
            'total_processed': (
                opened_result.get('n_inserted', 0) + 
                updated_result.get('n_updated', 0)
            )
        }
    
    else:  # Durante o dia: apenas updates
        logger.info("Executando apenas updates incrementais")
        
        updated_result = LoadIncidentsUpdated(
            start_date=date_str,
            end_date=date_str
        ).run()
        
        return {
            'strategy': 'incremental_only',
            'updated_incidents': updated_result,
            'total_processed': updated_result.get('n_updated', 0)
        }
```

Esta task é essencial para manter o estado atual dos incidents atualizado durante o dia, capturando mudanças de estado, reatribuições, resoluções e outros updates críticos para o acompanhamento em tempo real.