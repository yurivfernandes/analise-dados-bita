from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()


urlpatterns = [
    path(
        "load-contract-sla/",
        LoadContractSLAView.as_view(),
        name="load-contract-sla",
    )
]

urlpatterns += router.urls
