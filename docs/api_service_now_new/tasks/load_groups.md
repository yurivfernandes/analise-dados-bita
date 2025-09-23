# LoadGroups

## Visão Geral

A task `LoadGroups` extrai grupos de usuários (sys_user_group) do ServiceNow. Estes grupos definem as equipes responsáveis por diferentes categorias de incidents e representam a estrutura organizacional para atribuição de trabalho.

## Características

- **Tipo**: Task de Configurações (sem período)
- **Modelo**: `Groups`
- **Filtro Principal**: Nome do grupo
- **Estratégia de Carga**: UPSERT (preserva timestamps ETL)
- **Frequência**: Dados relativamente estáticos, executados esporadicamente

## Implementação

### Classe Principal

```python
class LoadGroups(MixinGetDataset, Pipeline):
    def __init__(self):
        super().__init__()
```

### Query ServiceNow

```python
params = {"sysparm_fields": fields, "sysparm_query": "nameSTARTSWITHvita"}

result_list = paginate(
    path="sys_user_group",
    params=params,
    limit=10000,
    mode="offset",
    limit_param="sysparm_limit",
    offset_param="sysparm_offset",
    result_key="result",
)
```

**Filtros Aplicados**:
- `nameSTARTSWITHvita` - Grupos que começam com "vita"

**Diferença das Tasks de Incidents**: Não filtra por data, busca todos os grupos ativos.

## Estrutura de Grupos

### Campos Principais

**Identificação**:
- `sys_id` (PK) - ID único do grupo
- `name` - Nome do grupo
- `description` - Descrição detalhada

**Configuração**:
- `manager` - Gerente do grupo (referência a sys_user)
- `parent` - Grupo pai (hierarquia)
- `type` - Tipo do grupo

**Contatos**:
- `email` - Email do grupo
- `phone` - Telefone de contato

**Status**:
- `active` - Grupo ativo (true/false)
- `include_members` - Incluir membros (true/false)

**Workflow**:
- `default_assignee` - Responsável padrão para atribuições
- `exclude_manager` - Excluir gerente das atribuições

### Exemplo de Grupo

```json
{
  "sys_id": "group_123abc",
  "name": "Vita - Infrastructure Team",
  "description": "Equipe responsável por servidores e infraestrutura",
  "manager": "usr_456def",
  "parent": "vita_parent_group",
  "email": "infra@vita.com.br",
  "phone": "+5511999887766",
  "active": "true",
  "include_members": "true",
  "default_assignee": "usr_789ghi"
}
```

## Tipos de Grupos Típicos

### Por Especialidade Técnica

```
Vita - Network Team           (Redes e conectividade)
Vita - Server Team            (Servidores e virtualização)
Vita - Database Team          (Bancos de dados)
Vita - Security Team          (Segurança da informação)
Vita - Application Support    (Suporte a aplicações)
```

### Por Nível de Suporte

```
Vita - L1 Support            (Primeiro nível)
Vita - L2 Support            (Segundo nível)
Vita - L3 Support            (Terceiro nível/especialistas)
Vita - Emergency Response    (Emergências)
```

### Por Horário/Localização

```
Vita - Business Hours        (Horário comercial)
Vita - 24x7 Operations       (Operações 24 horas)
Vita - Weekend Support       (Suporte fins de semana)
Vita - Night Shift           (Turno noturno)
```

## Estratégia UPSERT

### Diferença das Tasks de Incidents

```python
def run(self) -> Dict:
    self.extract_and_transform_dataset()
    upsert_by_sys_id(dataset=self.dataset, model=Groups, log=self.log)
    return self.log
```

**Vantagens do UPSERT**:
- **Preserva Timestamps**: `etl_created_at` mantém valor original
- **Performance**: Não deleta/recria registros inalterados
- **Histórico**: Mantém auditoria de quando cada grupo foi criado
- **Incremental**: Apenas insere novos ou atualiza modificados

### Processo UPSERT

```python
# 1. Busca grupos existentes no banco
existing = {o.sys_id: o for o in Groups.objects.filter(sys_id__in=[...])}

# 2. Separa operações
to_create = []  # Novos grupos
to_update = []  # Grupos existentes modificados

# 3. Para cada grupo do ServiceNow
for group_data in dataset:
    if group_data['sys_id'] in existing:
        # Verifica se houve mudanças
        existing_obj = existing[group_data['sys_id']]
        if has_changes(existing_obj, group_data):
            to_update.append(update_object(existing_obj, group_data))
    else:
        to_create.append(Groups(**group_data))

# 4. Executa bulk operations
Groups.objects.bulk_create(to_create, batch_size=1000)
Groups.objects.bulk_update(to_update, fields, batch_size=1000)
```

## Relacionamentos

### Com Incidents

```python
# Incidents atribuídos a um grupo
group = Groups.objects.get(name="Vita - Infrastructure Team")
incidents = Incident.objects.filter(assignment_group=group.sys_id)

print(f"Incidents ativos do grupo {group.name}: {incidents.count()}")

# Distribuição por estado
from django.db.models import Count
distribution = incidents.values('state').annotate(
    count=Count('sys_id')
).order_by('state')

for item in distribution:
    print(f"Estado {item['state']}: {item['count']} incidents")
```

### Com IncidentTask

```python
# Tasks atribuídas ao grupo
tasks = IncidentTask.objects.filter(assignment_group=group.sys_id)

# Tasks por estado
task_states = tasks.values('state').annotate(
    count=Count('sys_id')
).order_by('state')
```

### Hierarquia de Grupos

```python
# Grupos filhos de um grupo pai
parent_group = Groups.objects.get(name="Vita - Technical Support")
child_groups = Groups.objects.filter(parent=parent_group.sys_id)

print(f"Grupos filhos de {parent_group.name}:")
for child in child_groups:
    print(f"  - {child.name}")

# Árvore hierárquica
def build_group_hierarchy(parent_id=None, level=0):
    groups = Groups.objects.filter(parent=parent_id, active='true')
    
    for group in groups:
        print("  " * level + f"- {group.name}")
        build_group_hierarchy(group.sys_id, level + 1)

# Começar da raiz
build_group_hierarchy()
```

## Performance

### Métricas Típicas

| Métrica | Valor Típico | Observações |
|---------|--------------|-------------|
| **Volume Total** | 20-100 grupos | Estrutura organizacional estável |
| **Novos por Execução** | 0-2 grupos | Raramente criados |
| **Modificados** | 1-5 grupos | Ocasionalmente ajustados |
| **Tempo de Execução** | 5-15 segundos | Muito rápido |

### Frequência de Execução

```python
# ✅ Recomendado: Diário ou semanal
# Estrutura de grupos muda pouco

# ⚠️ Aceitável: Durante carga de incidents  
# Para garantir grupos atualizados

# ❌ Desnecessário: Múltiplas vezes por dia
# Waste de recursos para dados estruturais
```

## Uso Prático

### Análise de Workload por Grupo

```python
from datetime import date, timedelta
from django.db.models import Count, Avg

def group_workload_analysis(days_back=7):
    """Análise de carga de trabalho por grupo"""
    
    start_date = date.today() - timedelta(days=days_back)
    
    # Incidents por grupo nos últimos N dias
    incident_stats = Incident.objects.filter(
        opened_at__date__gte=start_date
    ).values(
        'assignment_group'
    ).annotate(
        incident_count=Count('sys_id'),
        avg_priority=Avg('priority')
    ).order_by('-incident_count')
    
    result = []
    for stat in incident_stats:
        group = Groups.objects.filter(sys_id=stat['assignment_group']).first()
        if group:
            result.append({
                'group_name': group.name,
                'incident_count': stat['incident_count'],
                'avg_priority': round(stat['avg_priority'] or 0, 2),
                'workload_score': calculate_workload_score(stat)
            })
    
    return result

def calculate_workload_score(stats):
    """Calcula score de carga baseado em volume e prioridade"""
    base_score = stats['incident_count']
    priority_weight = (5 - (stats['avg_priority'] or 3)) * 0.2
    return round(base_score * (1 + priority_weight), 1)
```

### Dashboard de Grupos

```python
def groups_dashboard():
    """Dashboard de status dos grupos"""
    
    active_groups = Groups.objects.filter(active='true')
    
    dashboard_data = {
        'total_groups': active_groups.count(),
        'groups_with_manager': active_groups.exclude(
            manager__isnull=True
        ).exclude(manager='').count(),
        'groups_by_parent': {},
        'recent_incidents_by_group': {}
    }
    
    # Agrupa por parent
    for group in active_groups:
        parent_name = "Root"
        if group.parent:
            parent_group = Groups.objects.filter(sys_id=group.parent).first()
            parent_name = parent_group.name if parent_group else "Unknown Parent"
        
        dashboard_data['groups_by_parent'].setdefault(parent_name, []).append({
            'name': group.name,
            'has_manager': bool(group.manager),
            'has_email': bool(group.email)
        })
    
    # Incidents recentes por grupo
    recent_incidents = Incident.objects.filter(
        opened_at__date__gte=date.today() - timedelta(days=1)
    ).values('assignment_group').annotate(
        count=Count('sys_id')
    ).order_by('-count')[:10]
    
    for item in recent_incidents:
        group = Groups.objects.filter(sys_id=item['assignment_group']).first()
        if group:
            dashboard_data['recent_incidents_by_group'][group.name] = item['count']
    
    return dashboard_data
```

## Configuração e Filtros

### Filtros Customizáveis

O filtro atual é hardcoded:

```python
params = {"sysparm_fields": fields, "sysparm_query": "nameSTARTSWITHvita"}
```

**Possível Melhoria**:

```python
# Em settings.py
SERVICENOW_GROUP_FILTERS = [
    'vita',
    'vgr', 
    'bradesco',
    'internal'
]

# Na task
filter_conditions = [f"nameSTARTSWITH{prefix}" for prefix in settings.SERVICENOW_GROUP_FILTERS]
query = "^OR".join(filter_conditions)
```

### Campos Extraídos

```python
fields = ",".join([
    f.name for f in Groups._meta.fields 
    if not f.name.startswith("etl_") and f.name != "etl_hash"
])

# Campos típicos incluídos:
# sys_id, name, description, manager, parent,
# email, phone, active, include_members,
# default_assignee, exclude_manager, etc.
```

## Monitoramento

### Métricas de Estrutura Organizacional

```python
from django.utils import timezone
from datetime import timedelta

def organizational_health_check():
    """Verificação da saúde da estrutura organizacional"""
    
    active_groups = Groups.objects.filter(active='true')
    issues = []
    
    # 1. Grupos sem gerente
    no_manager = active_groups.filter(
        Q(manager__isnull=True) | Q(manager='')
    ).count()
    
    if no_manager > 0:
        issues.append(f"{no_manager} grupos sem gerente definido")
    
    # 2. Grupos sem email
    no_email = active_groups.filter(
        Q(email__isnull=True) | Q(email='')
    ).count()
    
    if no_email > 0:
        issues.append(f"{no_email} grupos sem email de contato")
    
    # 3. Grupos órfãos (parent inexistente)
    orphaned = []
    for group in active_groups.exclude(parent__isnull=True).exclude(parent=''):
        if not Groups.objects.filter(sys_id=group.parent).exists():
            orphaned.append(group.name)
    
    if orphaned:
        issues.append(f"Grupos órfãos: {', '.join(orphaned[:5])}")
    
    # 4. Grupos sem incidents recentes (pode indicar inatividade)
    recent_threshold = timezone.now() - timedelta(days=30)
    inactive_groups = []
    
    for group in active_groups:
        recent_incidents = Incident.objects.filter(
            assignment_group=group.sys_id,
            opened_at__gte=recent_threshold
        ).exists()
        
        if not recent_incidents:
            inactive_groups.append(group.name)
    
    if len(inactive_groups) > 5:  # Threshold ajustável
        issues.append(f"{len(inactive_groups)} grupos sem incidents recentes")
    
    return {
        'total_active_groups': active_groups.count(),
        'issues_found': len(issues),
        'issues': issues,
        'health_score': calculate_health_score(active_groups.count(), len(issues))
    }

def calculate_health_score(total_groups, issues_count):
    """Calcula score de saúde organizacional (0-100)"""
    if total_groups == 0:
        return 0
    
    base_score = 100
    penalty_per_issue = 20
    score = max(0, base_score - (issues_count * penalty_per_issue))
    
    return score
```

### Alertas de Configuração

```python
def configuration_alerts():
    """Alertas de configuração dos grupos"""
    
    alerts = []
    
    # Novos grupos criados recentemente
    recent_groups = Groups.objects.filter(
        etl_created_at__gte=timezone.now() - timedelta(days=7)
    )
    
    if recent_groups.exists():
        alerts.append({
            'type': 'new_groups',
            'message': f'{recent_groups.count()} novos grupos criados',
            'groups': [g.name for g in recent_groups]
        })
    
    # Grupos modificados recentemente
    modified_groups = Groups.objects.filter(
        etl_updated_at__gte=timezone.now() - timedelta(days=7)
    ).exclude(
        etl_created_at__gte=timezone.now() - timedelta(days=7)
    )
    
    if modified_groups.exists():
        alerts.append({
            'type': 'modified_groups',
            'message': f'{modified_groups.count()} grupos modificados',
            'groups': [g.name for g in modified_groups]
        })
    
    return alerts
```

## Integração com Outras Tasks

### Dependências

```python
# LoadGroups deve executar ANTES das tasks de incidents
# Para garantir que os grupos existam quando incidents forem processados

execution_order = [
    'LoadGroups',           # 1º - Estrutura organizacional
    'LoadSysUser',          # 2º - Usuários
    'LoadIncidentsOpened',  # 3º - Incidents (usa grupos)
    'LoadIncidentTask',     # 4º - Tasks (usa grupos)
]
```

### Validação de Integridade

```python
def validate_group_references():
    """Valida integridade referencial com groups"""
    
    # Incidents com assignment_group inválido
    invalid_incidents = Incident.objects.extra(
        where=["assignment_group NOT IN (SELECT sys_id FROM groups WHERE active = 'true')"]
    ).filter(
        assignment_group__isnull=False
    ).exclude(assignment_group='')
    
    if invalid_incidents.exists():
        logger.warning(f"Incidents com grupos inválidos: {invalid_incidents.count()}")
        
        # Top 5 grupos mais referenciados mas inexistentes
        missing_groups = invalid_incidents.values('assignment_group').annotate(
            count=Count('sys_id')
        ).order_by('-count')[:5]
        
        for item in missing_groups:
            logger.warning(f"Grupo inexistente: {item['assignment_group']} ({item['count']} incidents)")
    
    return invalid_incidents.count()
```

Esta task é fundamental para manter a estrutura organizacional atualizada e garantir que as atribuições de incidents tenham grupos válidos.