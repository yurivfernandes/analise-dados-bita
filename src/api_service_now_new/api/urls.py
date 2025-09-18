from django.urls import path

from .views import LoadConfigurationsView, LoadIncidentsView

urlpatterns = [
    path(
        "load-incidents/", LoadIncidentsView.as_view(), name="load-incidents"
    ),
    path(
        "load-configurations/",
        LoadConfigurationsView.as_view(),
        name="load-configurations",
    ),
]
