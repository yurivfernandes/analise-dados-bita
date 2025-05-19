from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(
    "solar-new-id",
    viewset=SolarInterfacesVGR,
    basename="solar-new-id",
)

urlpatterns = []

urlpatterns += router.urls
