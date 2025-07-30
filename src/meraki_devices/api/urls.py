from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(
    "meraki-device",
    viewset=MerakiDeviceView,
    basename="meraki-device",
)

urlpatterns = [
    path(
        "load-meraki-device/",
        LoadMerakiDevicesView.as_view(),
        name="load-meraki-device",
    )
]

urlpatterns += router.urls
