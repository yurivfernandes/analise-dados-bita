from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    path(
        "load-incidents/",
        views.LoadIncidentsView.as_view(),
        name="load-incidents",
    )
]

urlpatterns += router.urls
