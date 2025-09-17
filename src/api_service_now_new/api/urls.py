from django.urls import path

from .views import LoadConfigurationsView, LoadIncidentsView

urlpatterns = [
    path(
        "load_incidents/", LoadIncidentsView.as_view(), name="load_incidents"
    ),
    path(
        "load_configurations/",
        LoadConfigurationsView.as_view(),
        name="load_configurations",
    ),
]
