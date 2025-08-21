from django.urls import path

from . import views

urlpatterns = [
    path(
        "load_capacity_datacenter/",
        views.LoadCapacityDatacenterView.as_view(),
        name="load_capacity_datacenter",
    ),
]
