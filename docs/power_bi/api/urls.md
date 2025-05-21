# API - URLs

Este arquivo documenta as rotas principais expostas pelo app **power_bi**.

## Exemplo de registro de rota com router DRF

```python
from rest_framework.routers import DefaultRouter
from .views import SolarInterfacesVGR, SolarIDVGRInterfaceVGRCorrigido, LoadInterfaceNewIDVGR

router = DefaultRouter()
router.register(
    "solar-interfaces-vgr",
    viewset=SolarInterfacesVGR,
    basename="solar-new-id",
)
router.register(
    "solar-id-vgr-interface-vgr-corrigido",
    viewset=SolarIDVGRInterfaceVGRCorrigido,
    basename="solar-new-id",
)

urlpatterns = [
    path(
        "load-interface-new-id-vgr/",
        view=LoadInterfaceNewIDVGR.as_view(),
        name="interfaces-new",
    ),
]
urlpatterns += router.urls
```

- Cada rota registrada expõe um endpoint RESTful para o recurso correspondente.
- Para adicionar novas rotas, registre novos viewsets no router.
