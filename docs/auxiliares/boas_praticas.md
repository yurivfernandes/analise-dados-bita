# Boas Práticas em Projetos Django Backend

## Estrutura do Projeto

### Organização de Apps
```python
projeto/
    ├── app1/
    │   ├── api/
    │   │   ├── views/
    │   │   ├── serializers/
    │   │   └── urls.py
    │   ├── models/
    │   └── tasks/
    └── app2/
        └── ...
```

## Models

### 1. Nomenclatura
- Use nomes em inglês
- Classes em PascalCase
- Campos em snake_case
- Seja descritivo nos nomes

```python
# Bom
class CustomerOrder(models.Model):
    order_date = models.DateTimeField()

# Ruim
class Pedido(models.Model):
    dt = models.DateTimeField()
```

### 2. Organização de Campos
- Campos mais importantes primeiro
- Campos de auditoria por último
- Use comentários para campos complexos

```python
class Order(models.Model):
    # Campos principais
    number = models.CharField(max_length=50)
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    
    # Campos de status
    status = models.CharField(max_length=20)
    
    # Campos de auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3. Índices e Performance
- Crie índices para campos frequentemente filtrados
- Use `db_index=True` com moderação
- Implemente `Meta.indexes` para índices compostos

```python
class Meta:
    indexes = [
        models.Index(fields=['status', 'created_at']),
    ]
```

## Views

### 1. Organização
- Separe views por funcionalidade
- Use ViewSets para CRUD padrão
- Implemente views específicas para casos especiais

### 2. Performance
- Use `select_related()` e `prefetch_related()`
- Implemente paginação
- Cache quando apropriado

```python
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer')
    pagination_class = CustomPagination
```

### 3. Segurança
- Sempre use decorators de permissão
- Valide dados de entrada
- Use rate limiting

```python
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
def sensitive_view(request):
    # ...
```

## Pipelines

### 1. Design
- Siga o princípio de responsabilidade única
- Use context managers
- Implemente logs detalhados

```python
class DataPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def extract(self):
        self.logger.info("Iniciando extração")
        # ...
```

### 2. Tratamento de Erros
- Use transações atômicas
- Implemente rollback
- Mantenha logs de erro

```python
@transaction.atomic
def process_data(self):
    try:
        # processamento
        self.save()
    except Exception as e:
        self.logger.error(f"Erro: {str(e)}")
        raise
```

## Configurações do Projeto

### 1. Variáveis de Ambiente
- Use `.env` para configurações sensíveis
- Mantenha um `.env.example` no repositório
- Documente todas as variáveis

```python
# settings.py
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### 2. Múltiplos Ambientes
- Separe settings por ambiente (dev, prod, test)
- Use arquivos de requirements específicos
- Configure logging apropriadamente

## Migrações

### 1. Boas Práticas
- Revise migrações antes de commit
- Mantenha migrações pequenas e atômicas
- Use `db_constraint=False` com cautela

### 2. Operações Sensíveis
- Evite migrações que podem travar tabelas
- Planeje migrações de dados grandes
- Teste migrações em ambiente de desenvolvimento

## Links Úteis

### Django
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)
- [Django REST framework](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Django ORM Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

### Python
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Design Patterns](https://python-patterns.guide/)

### Segurança
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Performance
- [Django Database Performance](https://docs.djangoproject.com/en/stable/topics/performance/)
- [REST Framework Throttling](https://www.django-rest-framework.org/api-guide/throttling/)

## Ferramentas Recomendadas

### Desenvolvimento
- **Black**: Formatação de código
- **Flake8**: Linting
- **isort**: Organização de imports
- **mypy**: Verificação de tipos

### Testes
- **pytest**: Framework de testes
- **coverage**: Cobertura de testes
- **factory_boy**: Factories para testes

### Documentação
- **mkdocs**: Documentação do projeto
- **drf-yasg**: Documentação de API

## Checklist de Revisão de Código

- [ ] O código segue PEP 8?
- [ ] As migrações foram testadas?
- [ ] Há testes unitários?
- [ ] A documentação foi atualizada?
- [ ] As queries estão otimizadas?
- [ ] As permissões estão configuradas?
- [ ] O código está logando apropriadamente?
- [ ] As exceções são tratadas adequadamente?
