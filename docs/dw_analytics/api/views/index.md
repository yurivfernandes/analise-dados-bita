# Views

## O que são views em Python/Django?

No contexto do Django, **views** são funções ou classes responsáveis por receber uma requisição HTTP, processar dados (consultar banco, aplicar regras de negócio, etc.) e retornar uma resposta HTTP (geralmente JSON em APIs).

- Em APIs REST, as views geralmente herdam de classes do Django REST Framework, como `APIView` ou `ModelViewSet`.

---

## Estrutura básica de uma view

### Exemplo de função view

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def minha_view(request):
    data = {"mensagem": "Olá, mundo!"}
    return Response(data)
```

### Exemplo de viewset (CRUD completo)

```python
from rest_framework.viewsets import ModelViewSet
from .models import FIncidentsBita
from .serializers import FIncidentsBitaSerializer

class FIncidentsBitaViewset(ModelViewSet):
    queryset = FIncidentsBita.objects.all()
    serializer_class = FIncidentsBitaSerializer
```

---

## Onde importar e por que importar views nos `__init__.py`

- As views devem ser importadas no `__init__.py` do módulo para facilitar o import em outros lugares (ex: arquivos de rotas/urls).
- Isso permite importar todas as views do app com uma única linha, mantendo o código organizado e evitando importações circulares.

**Exemplo:**
```python
# dw_analytics/api/views/__init__.py
from .f_incidents_bita_viewset import FIncidentsBitaViewset
```

---

## Relação entre views Python e views SQL

- **Views em SQL**: São consultas salvas no banco de dados, que podem ser usadas como tabelas virtuais para facilitar consultas complexas.
- **Views em Django/Python**: São pontos de entrada para requisições HTTP, podendo retornar dados de qualquer fonte (incluindo views SQL, tabelas, arquivos, etc).

**Paralelo:**  
- Uma view SQL encapsula uma consulta;  
- Uma view Python encapsula uma lógica de negócio e pode, inclusive, consultar uma view SQL para retornar dados.

---

## Como construir uma view

1. **Defina o que a view deve fazer** (listar, criar, atualizar, deletar, etc).
2. **Implemente como função ou classe** (preferencialmente classe para CRUD).
3. **Implemente o serializer** para transformar modelos em JSON.
4. **Registre a view no arquivo de rotas (`urls.py`)**.

---

## Exemplo prático

```python
# views/f_incidents_bita_viewset.py
from rest_framework.viewsets import ModelViewSet
from ...models import FIncidentsBita
from ..serializers import FIncidentsBitaSerializer

class FIncidentsBitaViewset(ModelViewSet):
    queryset = FIncidentsBita.objects.all()
    serializer_class = FIncidentsBitaSerializer
```

```python
# api/urls.py
from rest_framework.routers import DefaultRouter
from .views import FIncidentsBitaViewset

router = DefaultRouter()
router.register("f-incidents-bita", FIncidentsBitaViewset)
urlpatterns = router.urls
```

---

## Resumo

- Views Python são responsáveis por processar requisições e retornar respostas.
- São essenciais para expor dados do banco (inclusive views SQL) via API.
- Devem ser importadas nos `__init__.py` para facilitar a organização e o uso em rotas.
- A estrutura básica envolve herdar de classes do DRF e registrar as views nas rotas do app.
