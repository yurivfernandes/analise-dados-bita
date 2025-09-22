# LoadTaskTimeWorked

## Visão Geral

A task `LoadTaskTimeWorked` extrai registros de tempo trabalhado em tasks do ServiceNow. Estes dados são essenciais para análises de produtividade, cobrança de horas, e métricas de eficiência das equipes.

## Características

- **Tipo**: Task de Incidents (com período)
- **Modelo**: `TaskTimeWorked`
- **Filtro Principal**: `sys_created_on` (data de criação do registro)
- **Estratégia de Carga**: DELETE + INSERT (transacional)
- **Relacionamento**: Conecta com `IncidentTask` via campo `task`

## Implementação

### Classe Principal

```python
class LoadTaskTimeWorked(MixinGetDataset, Pipeline):
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date  # YYYY-MM-DD
        self.end_date = end_date      # YYYY-MM-DD
        super().__init__()
```

### Query ServiceNow

```python
query = f"sys_created_on>={self.start_date} 00:00:00^sys_created_on<={self.end_date} 23:59:59"
```

**Características da Query**:
- Filtra por `sys_created_on` (quando o registro de tempo foi criado)
- **Não usa filtro de grupo** específico (diferente de outras tasks)
- Captura todos os registros de tempo do período

## Estrutura de Dados

### Campos Principais

O modelo `TaskTimeWorked` inclui:

**Identificação**:
- `sys_id` (PK) - ID único do registro de tempo
- `task` - Referência à task (sys_id)

**Tempo Trabalhado**:
- `time_spent` - Tempo gasto (em horas, formato decimal)
- `work_start` - Data/hora de início do trabalho
- `work_end` - Data/hora de fim do trabalho

**Descrição**:
- `short_description` - Descrição breve do trabalho realizado
- `work_notes` - Notas detalhadas do trabalho

**Usuário**:
- `created_by` - Quem registrou o tempo
- `user` - Usuário que executou o trabalho (pode ser diferente do created_by)

**Auditoria**:
- `sys_created_on`, `sys_created_by`
- `sys_updated_on`, `sys_updated_by`

### Exemplo de Registro

```json
{
  "sys_id": "time123abc",
  "task": "task456def", 
  "time_spent": "2.5",
  "work_start": "2025-01-20 09:00:00",
  "work_end": "2025-01-20 11:30:00",
  "short_description": "Configuração de firewall",
  "work_notes": "Configurei as regras de firewall conforme solicitado. Testei conectividade e documentei as mudanças.",
  "created_by": "usr789ghi",
  "user": "usr789ghi",
  "sys_created_on": "2025-01-20 11:35:00"
}
```

## Relacionamentos

### Com IncidentTask

```python
# Buscar tempo total trabalhado em uma task
task = IncidentTask.objects.get(number="TASK0001234")
time_records = TaskTimeWorked.objects.filter(task=task.sys_id)

total_hours = sum([
    float(record.time_spent) for record in time_records 
    if record.time_spent
])

print(f"Tempo total na task {task.number}: {total_hours}h")
```

### Com Incident (via Task)

```python
# Tempo total trabalhado em um incident (soma de todas as tasks)
incident = Incident.objects.get(number="INC0001234")

# Busca todas as tasks do incident
incident_tasks = IncidentTask.objects.filter(parent=incident.sys_id)

total_incident_time = 0
for task in incident_tasks:
    task_time_records = TaskTimeWorked.objects.filter(task=task.sys_id)
    task_total = sum([
        float(record.time_spent or 0) for record in task_time_records
    ])
    total_incident_time += task_total

print(f"Tempo total no incident {incident.number}: {total_incident_time}h")
```

### Com Usuários

```python
# Produtividade por usuário
from django.db.models import Sum
from django.db import connection

user_productivity = TaskTimeWorked.objects.filter(
    sys_created_on__date='2025-01-20'
).values('created_by').annotate(
    total_time=Sum('time_spent'),
    task_count=Count('task', distinct=True)
).order_by('-total_time')

for record in user_productivity:
    if record['created_by']:
        user = SysUser.objects.filter(sys_id=record['created_by']).first()
        user_name = user.name if user else f"ID: {record['created_by']}"
        avg_time_per_task = record['total_time'] / record['task_count'] if record['task_count'] else 0
        
        print(f"{user_name}:")
        print(f"  Total: {record['total_time']:.1f}h")
        print(f"  Tasks: {record['task_count']}")
        print(f"  Média/task: {avg_time_per_task:.1f}h")
```

## Análises e Métricas

### 1. Produtividade Diária

```python
def daily_productivity_report(date_target):
    """Relatório de produtividade diária por usuário"""
    
    daily_stats = TaskTimeWorked.objects.filter(
        sys_created_on__date=date_target
    ).aggregate(
        total_hours=Sum('time_spent'),
        total_records=Count('sys_id'),
        unique_users=Count('created_by', distinct=True),
        unique_tasks=Count('task', distinct=True)
    )
    
    # Top 10 usuários por horas trabalhadas
    top_users = TaskTimeWorked.objects.filter(
        sys_created_on__date=date_target
    ).values('created_by').annotate(
        hours=Sum('time_spent')
    ).order_by('-hours')[:10]
    
    return {
        'summary': daily_stats,
        'top_users': list(top_users)
    }
```

### 2. Eficiência por Tipo de Task

```python
def task_efficiency_analysis():
    """Analisa eficiência por tipo de task baseado em descrições"""
    
    # Categoriza tasks por palavras-chave
    categories = {
        'firewall': ['firewall', 'iptables', 'security'],
        'server': ['server', 'servidor', 'vm'], 
        'network': ['network', 'rede', 'switch', 'router'],
        'database': ['database', 'db', 'sql', 'mysql']
    }
    
    efficiency_data = {}
    
    for category, keywords in categories.items():
        # Tasks que contêm palavras-chave
        task_filter = Q()
        for keyword in keywords:
            task_filter |= Q(short_description__icontains=keyword)
        
        time_records = TaskTimeWorked.objects.filter(
            task_filter,
            sys_created_on__date__gte=date.today() - timedelta(days=30)
        )
        
        if time_records.exists():
            stats = time_records.aggregate(
                avg_time=Avg('time_spent'),
                total_time=Sum('time_spent'),
                record_count=Count('sys_id'),
                unique_tasks=Count('task', distinct=True)
            )
            
            efficiency_data[category] = {
                'avg_time_per_record': stats['avg_time'] or 0,
                'total_time': stats['total_time'] or 0,
                'avg_time_per_task': (stats['total_time'] / stats['unique_tasks']) if stats['unique_tasks'] else 0,
                'record_count': stats['record_count'],
                'task_count': stats['unique_tasks']
            }
    
    return efficiency_data
```

### 3. Análise de Overtime

```python
def overtime_analysis(date_start, date_end):
    """Identifica possível overtime baseado em horários"""
    
    # Registros fora do horário comercial (antes 8h ou após 18h)
    overtime_records = TaskTimeWorked.objects.extra(
        where=[
            "EXTRACT(hour FROM work_start::timestamp) < 8 OR EXTRACT(hour FROM work_end::timestamp) > 18"
        ]
    ).filter(
        sys_created_on__date__range=[date_start, date_end],
        work_start__isnull=False,
        work_end__isnull=False
    )
    
    overtime_by_user = overtime_records.values('created_by').annotate(
        overtime_hours=Sum('time_spent'),
        overtime_sessions=Count('sys_id')
    ).order_by('-overtime_hours')
    
    return list(overtime_by_user)
```

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Diário** | 200-1000 registros | Depende da disciplina das equipes |
| **Tempo Médio** | 1-3 minutos | Query simples, sem dot-walk |
| **Ratio Time/Task** | 0.5-2.0 | Registros de tempo por task |
| **Horas Médias/Registro** | 1-4 horas | Variável por tipo de trabalho |

### Características da Query

```python
# ✅ Query simples e rápida
query = "sys_created_on>=2025-01-20 00:00:00^sys_created_on<=2025-01-20 23:59:59"

# Não usa filtros de grupo (diferente de outras tasks)
# Captura TODOS os registros de tempo do período
```

**Vantagem**: Mais rápida que tasks com dot-walk ou filtros complexos

**Cuidado**: Pode capturar registros de grupos não-Vita

## Validações e Qualidade

### 1. Consistência Temporal

```python
def validate_time_consistency():
    """Valida consistência entre work_start, work_end e time_spent"""
    
    inconsistent = []
    
    time_records = TaskTimeWorked.objects.filter(
        work_start__isnull=False,
        work_end__isnull=False,
        time_spent__isnull=False,
        sys_created_on__date=date.today()
    )
    
    for record in time_records:
        try:
            start = datetime.fromisoformat(record.work_start.replace('Z', '+00:00'))
            end = datetime.fromisoformat(record.work_end.replace('Z', '+00:00'))
            
            duration_hours = (end - start).total_seconds() / 3600
            reported_hours = float(record.time_spent)
            
            # Diferença > 15 minutos é suspeita
            if abs(duration_hours - reported_hours) > 0.25:
                inconsistent.append({
                    'sys_id': record.sys_id,
                    'calculated': duration_hours,
                    'reported': reported_hours,
                    'difference': abs(duration_hours - reported_hours)
                })
                
        except (ValueError, TypeError):
            continue
    
    return inconsistent
```

### 2. Registros Órfãos

```python
def find_orphaned_time_records():
    """Encontra registros de tempo sem task válida"""
    
    orphaned = TaskTimeWorked.objects.extra(
        where=["task NOT IN (SELECT sys_id FROM incident_task)"]
    ).filter(
        sys_created_on__date__gte=date.today() - timedelta(days=7)
    )
    
    if orphaned.exists():
        logger.warning(f"Registros de tempo órfãos: {orphaned.count()}")
        
        # Detalhes dos órfãos
        for record in orphaned[:10]:  # Primeiros 10
            logger.debug(f"Órfão: {record.sys_id} → Task: {record.task}")
    
    return orphaned.count()
```

## Execução

### Standalone

```python
task = LoadTaskTimeWorked(
    start_date="2025-01-20",
    end_date="2025-01-20"
)

with task as loader:
    result = loader.run()
    
print(f"Registros de tempo: {result['n_inserted']}")
print(f"Duração: {result['duration']}s")

# Análise rápida dos dados carregados
today_records = TaskTimeWorked.objects.filter(sys_created_on__date='2025-01-20')
total_hours = sum([float(r.time_spent or 0) for r in today_records])
unique_users = today_records.values('created_by').distinct().count()

print(f"Total de horas registradas: {total_hours:.1f}h")
print(f"Usuários únicos: {unique_users}")
```

### Em Paralelo (LoadIncidentsView)

Executa simultaneamente com outras 3 tasks de incidents:

```python
heavy_tasks = [
    ("load_incidents_opened", LoadIncidentsOpened),
    ("load_incident_sla", LoadIncidentSla),
    ("load_task_time_worked", LoadTaskTimeWorked),  # Esta task
    ("load_incident_task", LoadIncidentTask),
]

# 4 threads paralelas
threads = []
for name, cls in heavy_tasks:
    th = threading.Thread(
        target=_run_task,
        args=(name, cls, start_date, end_date, results, errors),
        daemon=True
    )
    th.start()
    threads.append(th)
```

## Monitoramento

### KPIs de Tempo Trabalhado

```python
def time_tracking_kpis(target_date):
    """KPIs de tracking de tempo para dashboard"""
    
    records = TaskTimeWorked.objects.filter(sys_created_on__date=target_date)
    
    if not records.exists():
        return {'error': 'Nenhum registro de tempo encontrado'}
    
    # Estatísticas básicas
    total_records = records.count()
    total_hours = sum([float(r.time_spent or 0) for r in records])
    unique_users = records.values('created_by').distinct().count()
    unique_tasks = records.values('task').distinct().count()
    
    # Distribuição de horas
    hours_list = [float(r.time_spent) for r in records if r.time_spent]
    avg_hours = sum(hours_list) / len(hours_list) if hours_list else 0
    
    # Usuários mais produtivos
    top_users = records.values('created_by').annotate(
        hours=Sum('time_spent')
    ).order_by('-hours')[:5]
    
    return {
        'total_records': total_records,
        'total_hours': round(total_hours, 1),
        'unique_users': unique_users,
        'unique_tasks': unique_tasks,
        'avg_hours_per_record': round(avg_hours, 2),
        'records_per_user': round(total_records / unique_users, 1) if unique_users else 0,
        'hours_per_user': round(total_hours / unique_users, 1) if unique_users else 0,
        'top_users': list(top_users)
    }
```

### Alertas de Qualidade

```python
def quality_alerts(target_date):
    """Alertas de qualidade dos dados de tempo"""
    
    alerts = []
    records = TaskTimeWorked.objects.filter(sys_created_on__date=target_date)
    
    # 1. Volume muito baixo
    if records.count() < 50:  # Threshold ajustável
        alerts.append({
            'type': 'low_volume',
            'message': f'Volume baixo de registros: {records.count()}'
        })
    
    # 2. Muitos registros sem tempo
    no_time = records.filter(Q(time_spent__isnull=True) | Q(time_spent=''))
    if no_time.count() > records.count() * 0.1:  # >10%
        alerts.append({
            'type': 'missing_time',
            'message': f'{no_time.count()} registros sem tempo informado'
        })
    
    # 3. Registros com tempo excessivo
    high_time = records.extra(
        where=["CAST(time_spent AS FLOAT) > 12"]  # >12 horas
    )
    if high_time.exists():
        alerts.append({
            'type': 'excessive_time',
            'message': f'{high_time.count()} registros com >12h'
        })
    
    # 4. Falta de descrição
    no_desc = records.filter(
        Q(short_description__isnull=True) | 
        Q(short_description='')
    )
    if no_desc.count() > records.count() * 0.2:  # >20%
        alerts.append({
            'type': 'missing_description',
            'message': f'{no_desc.count()} registros sem descrição'
        })
    
    return alerts
```

## Troubleshooting

### Problemas Comuns

**1. Volume inconsistente**
```
Situação: Alguns dias com 0 registros, outros com centenas
Causa: Equipes não registram tempo consistentemente
Solução: Treinamento e políticas de time tracking
```

**2. Registros órfãos**
```
Situação: time_worked.task não existe em incident_task
Causa: Tasks deletadas após registros de tempo
Investigação: Validar integridade referencial
```

**3. Tempos irreais**
```
Situação: Registros com 24+ horas ou 0.1 horas
Causa: Erros de entrada de dados
Solução: Validações no ServiceNow
```

### Debug de Dados

```python
# Análise de qualidade dos dados carregados
def analyze_loaded_data(target_date):
    """Análise detalhada dos dados carregados"""
    
    records = TaskTimeWorked.objects.filter(sys_created_on__date=target_date)
    
    print(f"📊 Análise LoadTaskTimeWorked - {target_date}")
    print(f"Total de registros: {records.count()}")
    
    # Distribuição de tempo
    times = [float(r.time_spent) for r in records if r.time_spent]
    if times:
        print(f"Tempo total: {sum(times):.1f}h")
        print(f"Tempo médio: {sum(times)/len(times):.2f}h")
        print(f"Tempo mín/máx: {min(times):.2f}h / {max(times):.2f}h")
    
    # Top tasks por tempo
    top_tasks = records.values('task').annotate(
        total_time=Sum('time_spent')
    ).order_by('-total_time')[:5]
    
    print(f"\nTop 5 tasks por tempo:")
    for item in top_tasks:
        task = IncidentTask.objects.filter(sys_id=item['task']).first()
        task_name = task.number if task else f"ID: {item['task'][:8]}..."
        print(f"  {task_name}: {item['total_time']}h")
```

Esta task é crucial para análises de produtividade, cobrança de horas e otimização de processos, fornecendo insights detalhados sobre como o tempo é gasto na resolução de incidents.