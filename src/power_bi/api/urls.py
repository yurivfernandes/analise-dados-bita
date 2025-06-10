from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(
    "solar-interface",
    viewset=SolarInterface,
    basename="solar-interface",
)

urlpatterns = [
    path(
        "load-interface-vgr/",
        view=LoadInterfaceVGRView.as_view(),
        name="load-interface-vgr",
    ),
    path(
        "load-interface-original-vgr/",
        view=LoadInterfaceOriginalVGRView.as_view(),
        name="load-interface-original-vgr",
    ),
    path(
        "load-node-original-vgr/",
        view=LoadNodeOriginalVGRView.as_view(),
        name="load-node-original-vgr",
    ),
    path(
        "load-node-vgr/",
        view=LoadNodeVGRView.as_view(),
        name="load-node-vgr",
    ),
]

urlpatterns += router.urls
