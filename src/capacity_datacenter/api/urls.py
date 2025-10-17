from django.urls import path

from . import views

urlpatterns = [
    path(
        "load-capacity-datacenter/",
        views.LoadCapacityDatacenterView.as_view(),
        name="load-capacity-datacenter",
    ),
]
