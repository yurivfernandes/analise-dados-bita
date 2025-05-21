from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

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
