from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(
    "f-incidents-bita",
    viewset=FIncidentsBitaViewset,
    basename="f-incidents-bita",
)

urlpatterns = []

urlpatterns += router.urls
