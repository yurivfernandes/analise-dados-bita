# flatten_reference_fields()

## Visão Geral

A função `flatten_reference_fields()` é responsável por converter os campos de referência complexos do ServiceNow em valores simples utilizáveis pelos modelos Django. O ServiceNow retorna referências como objetos aninhados, mas nossos modelos precisam de valores string simples.

## Problema que Resolve

### Formato ServiceNow (Complexo)

O ServiceNow retorna referências em formato aninhado:

```json
{
  "sys_id": "inc123abc",
  "number": "INC0001234",
  "assignment_group": {
    "value": "grp456def",
    "display_value": "Vita Infrastructure Team",
    "link": "https://instance.service-now.com/api/now/table/sys_user_group/grp456def"
  },
  "assigned_to": {
    "value": "usr789ghi",
    "display_value": "João Silva",
    "link": "https://instance.service-now.com/api/now/table/sys_user/usr789ghi"
  },
  "priority": "1",
  "state": "2"
}
```

### Formato Django (Simples)

Nossos modelos Django esperam campos string simples:

```python
class Incident(models.Model):
    sys_id = models.TextField(primary_key=True)
    number = models.TextField()
    assignment_group = models.TextField()      # ← String simples, não objeto
    assigned_to = models.TextField()           # ← String simples
    priority = models.TextField()
    state = models.TextField()
```

## Implementação

### Assinatura

```python
def flatten_reference_fields(data: dict) -> dict:
    """Converte campos de referência do ServiceNow para valores simples"""
```

### Algoritmo

```python
def flatten_reference_fields(data: dict) -> dict:
    for key in list(data.keys()):
        value = data.get(key)
        
        # Verifica se é campo de referência ServiceNow
        if isinstance(value, dict) and "value" in value:
            # Extrai apenas o sys_id (value)
            data[key] = value.get("value")
            
            # Cria campo display_value separado
            data[f"dv_{key}"] = value.get("display_value", "")
    
    return data
```

## Transformação Detalhada

### Exemplo Passo a Passo

**Input**:
```json
{
  "sys_id": "inc123",
  "assignment_group": {
    "value": "grp456",
    "display_value": "Vita Infrastructure"
  },
  "priority": "1"
}
```

**Processamento**:
1. `key = "sys_id"`, `value = "inc123"` → Não é dict, mantém
2. `key = "assignment_group"`, `value = {"value": "grp456", ...}` → É referência!
   - `data["assignment_group"] = "grp456"` (sys_id)
   - `data["dv_assignment_group"] = "Vita Infrastructure"` (nome legível)
3. `key = "priority"`, `value = "1"` → Não é dict, mantém

**Output**:
```json
{
  "sys_id": "inc123",
  "assignment_group": "grp456",
  "dv_assignment_group": "Vita Infrastructure",
  "priority": "1"
}
```

### Campos Display Value

A função cria automaticamente campos `dv_*` para valores legíveis:

| Campo Original | Valor (sys_id) | Display Value | Uso |
|----------------|----------------|---------------|-----|
| `assignment_group` | `grp456def` | `dv_assignment_group` | "Vita Infrastructure Team" |
| `assigned_to` | `usr789ghi` | `dv_assigned_to` | "João Silva" |
| `manager` | `mgr123abc` | `dv_manager` | "Maria Santos" |
| `company` | `comp456def` | `dv_company` | "Vita Empresa LTDA" |

## Tipos de Referências

### 1. Referências de Usuário

```json
// ServiceNow Response
{
  "opened_by": {
    "value": "usr123abc", 
    "display_value": "João Silva"
  }
}

// Após flatten
{
  "opened_by": "usr123abc",
  "dv_opened_by": "João Silva"
}
```

### 2. Referências de Grupo

```json
// ServiceNow Response
{
  "assignment_group": {
    "value": "grp456def",
    "display_value": "Vita - Infrastructure Team"
  }
}

// Após flatten  
{
  "assignment_group": "grp456def",
  "dv_assignment_group": "Vita - Infrastructure Team"
}
```

### 3. Referências de Empresa

```json
// ServiceNow Response
{
  "company": {
    "value": "comp789ghi",
    "display_value": "Vita Tecnologia"
  }
}

// Após flatten
{
  "company": "comp789ghi", 
  "dv_company": "Vita Tecnologia"
}
```

### 4. Referências Aninhadas (SLA)

```json
// ServiceNow Response (IncidentSla)
{
  "task": {
    "value": "inc123abc",
    "display_value": "INC0001234"
  },
  "sla": {
    "value": "sla456def", 
    "display_value": "Vita - Priority 1 - Resolution"
  }
}

// Após flatten
{
  "task": "inc123abc",
  "dv_task": "INC0001234",
  "sla": "sla456def",
  "dv_sla": "Vita - Priority 1 - Resolution"
}
```

## Integração com Modelos

### Definição de Campos

Os modelos Django devem incluir campos `dv_*` para display values:

```python
class Incident(models.Model):
    # Campos de referência (sys_id)
    assignment_group = models.TextField(null=True, blank=True)
    assigned_to = models.TextField(null=True, blank=True)
    company = models.TextField(null=True, blank=True)
    
    # Campos display value (nomes legíveis) 
    dv_assignment_group = models.TextField(null=True, blank=True)
    dv_assigned_to = models.TextField(null=True, blank=True)
    dv_company = models.TextField(null=True, blank=True)
```

### Uso em Queries

```python
# Buscar incidents com informações legíveis
incidents = Incident.objects.filter(priority='1').values(
    'number',
    'assignment_group',        # sys_id → "grp456def" 
    'dv_assignment_group',     # nome → "Vita Infrastructure"
    'assigned_to',             # sys_id → "usr789ghi"
    'dv_assigned_to'           # nome → "João Silva"
)

for inc in incidents:
    print(f"Incident {inc['number']}")
    print(f"  Grupo: {inc['dv_assignment_group']} ({inc['assignment_group']})")
    print(f"  Atribuído: {inc['dv_assigned_to']} ({inc['assigned_to']})")
```

## Vantagens

### 1. Performance em Joins

```python
# ❌ Sem display values: JOIN necessário sempre
query = """
SELECT i.number, g.name as group_name
FROM incident i
JOIN groups g ON i.assignment_group = g.sys_id  
WHERE i.priority = '1'
"""

# ✅ Com display values: Consulta simples
query = """
SELECT number, dv_assignment_group as group_name  
FROM incident
WHERE priority = '1'
"""
```

### 2. Dados Self-Contained

Cada registro contém tanto o ID técnico quanto o nome legível:

```python
# Relatório sem necessidade de JOINs
incidents_report = Incident.objects.filter(
    opened_at__date='2025-01-20'
).values(
    'number',
    'dv_assignment_group',    # Nome do grupo
    'dv_assigned_to',         # Nome do usuário
    'dv_company',             # Nome da empresa
    'priority'
)

# DataFrame direto para análise
df = pd.DataFrame(incidents_report)
print(df.groupby('dv_assignment_group').size())
```

### 3. Tolerância a Referências Quebradas

```python
# Cenário: assignment_group foi deletado do ServiceNow
incident = Incident.objects.get(number='INC0001234')

print(f"Grupo ID: {incident.assignment_group}")        # "grp456def" (órfão)
print(f"Grupo Nome: {incident.dv_assignment_group}")   # "Vita Infrastructure" (preservado)

# Sem display values, perderia o nome do grupo
```

## Tratamento de Casos Especiais

### 1. Display Value Vazio

```python
# ServiceNow às vezes retorna display_value vazio
{
  "manager": {
    "value": "usr123abc",
    "display_value": ""    # ← Vazio
  }
}

# flatten_reference_fields garante string vazia, não None
{
  "manager": "usr123abc",
  "dv_manager": ""       # String vazia, não None
}
```

### 2. Referência Sem Display Value

```python
# Caso raro: apenas "value", sem "display_value"
{
  "company": {
    "value": "comp123abc"
    # display_value ausente
  }
}

# Resultado: display_value fica string vazia
{
  "company": "comp123abc", 
  "dv_company": ""
}
```

### 3. Referência Nula

```python
# Campo de referência nulo no ServiceNow
{
  "assigned_to": null
}

# Não é processado (não é dict com "value")
{
  "assigned_to": null    # Mantém null
}
```

## Casos de Uso Avançados

### 1. Análise sem JOINs

```python
def incident_summary_by_group():
    """Relatório de incidents por grupo sem JOIN"""
    
    summary = Incident.objects.filter(
        opened_at__date=date.today()
    ).values('dv_assignment_group').annotate(
        total=Count('sys_id'),
        priority_1=Count(Case(When(priority='1', then=1))),
        priority_2=Count(Case(When(priority='2', then=1))),
        priority_3=Count(Case(When(priority='3', then=1)))
    ).order_by('-total')
    
    return list(summary)

# Resultado direto sem JOIN
[
  {
    'dv_assignment_group': 'Vita Infrastructure',
    'total': 25,
    'priority_1': 5,
    'priority_2': 12, 
    'priority_3': 8
  },
  ...
]
```

### 2. Dashboard Queries

```python
def dashboard_data():
    """Dados para dashboard sem JOINs complexos"""
    
    today = date.today()
    
    return {
        # Top assignees
        'top_assignees': list(Incident.objects.filter(
            opened_at__date=today
        ).exclude(
            assigned_to__isnull=True
        ).values('dv_assigned_to').annotate(
            count=Count('sys_id')
        ).order_by('-count')[:10]),
        
        # Incidents by company  
        'by_company': list(Incident.objects.filter(
            opened_at__date=today
        ).values('dv_company').annotate(
            count=Count('sys_id')
        ).order_by('-count')),
        
        # SLA breach by group
        'sla_breach': list(IncidentSla.objects.filter(
            has_breached='true',
            sys_created_on__date=today
        ).values('dv_task').annotate(
            breached_slas=Count('sys_id')
        ))
    }
```

### 3. Export para Excel

```python
def export_incidents_to_excel():
    """Export com nomes legíveis"""
    
    incidents = Incident.objects.filter(
        opened_at__date=date.today()
    ).values(
        'number',
        'dv_assignment_group',
        'dv_assigned_to', 
        'dv_company',
        'priority',
        'state',
        'short_description'
    )
    
    df = pd.DataFrame(incidents)
    
    # Renomeia colunas para export
    df.rename(columns={
        'dv_assignment_group': 'Grupo',
        'dv_assigned_to': 'Atribuído Para',
        'dv_company': 'Empresa'
    }, inplace=True)
    
    df.to_excel('incidents_report.xlsx', index=False)
```

## Debugging

### Verificar Referências

```python
def debug_references(data_sample):
    """Analisa campos de referência em amostra de dados"""
    
    reference_fields = {}
    
    for record in data_sample:
        for key, value in record.items():
            if isinstance(value, dict) and "value" in value:
                if key not in reference_fields:
                    reference_fields[key] = {
                        'count': 0,
                        'examples': [],
                        'missing_display': 0
                    }
                
                reference_fields[key]['count'] += 1
                
                if not value.get('display_value'):
                    reference_fields[key]['missing_display'] += 1
                
                if len(reference_fields[key]['examples']) < 3:
                    reference_fields[key]['examples'].append({
                        'value': value.get('value'),
                        'display_value': value.get('display_value')
                    })
    
    return reference_fields

# Uso
sample = paginate("incident", params={"sysparm_limit": "100"})
refs = debug_references(sample)
for field, stats in refs.items():
    print(f"{field}: {stats['count']} referências")
    if stats['missing_display'] > 0:
        print(f"  ⚠️  {stats['missing_display']} sem display_value")
```

### Comparar Antes/Depois

```python
def compare_flatten_impact(original_data):
    """Compara dados antes e depois do flatten"""
    
    original_count = len(original_data)
    original_fields = set()
    
    for record in original_data:
        original_fields.update(record.keys())
    
    # Aplica flatten
    flattened_data = [flatten_reference_fields(dict(record)) for record in original_data]
    
    flattened_fields = set()
    for record in flattened_data:
        flattened_fields.update(record.keys())
    
    new_fields = flattened_fields - original_fields
    dv_fields = [f for f in new_fields if f.startswith('dv_')]
    
    print(f"Registros: {original_count}")
    print(f"Campos originais: {len(original_fields)}")  
    print(f"Campos após flatten: {len(flattened_fields)}")
    print(f"Novos campos dv_*: {len(dv_fields)}")
    print(f"Campos dv_* criados: {sorted(dv_fields)}")
```

Esta função é fundamental para tornar os dados do ServiceNow utilizáveis em modelos Django, convertendo estruturas complexas em campos simples enquanto preserva informações legíveis através dos campos display value.