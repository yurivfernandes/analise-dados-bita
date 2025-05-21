# API - URLs

Este arquivo documenta as rotas principais expostas pelo app **dw_analytics**.

## Exemplo de registro de rota com router DRF

```python
from rest_framework.routers import DefaultRouter
from .views import FIncidentsBitaViewset

router = DefaultRouter()
router.register(
    "f-incidents-bita",
    viewset=FIncidentsBitaViewset,
    basename="f-incidents-bita",
)

urlpatterns = []
urlpatterns += router.urls
```

- Cada rota registrada expõe um endpoint RESTful para o recurso correspondente.
- Para adicionar novas rotas, registre novos viewsets no router.
