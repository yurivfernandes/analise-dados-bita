from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(
    "f-incidents-bita",
    viewset=FIncidentsBitaViewset,
    basename="f-incidents-bita",
)
router.register("incidents", viewset=IncidentViewSet, basename="incidents")

urlpatterns = [
    path(
        "incident-fields/",
        FIncidentFieldsView.as_view(),
        name="incident-fields",
    ),
]

urlpatterns += router.urls
