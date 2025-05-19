from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(
    "solar-interfaces-vgr",
    viewset=SolarInterfacesVGR,
    basename="solar-new-id",
)

urlpatterns = []

urlpatterns += router.urls
