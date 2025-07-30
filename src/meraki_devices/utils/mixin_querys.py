from django.db.models import QuerySet

from ..models import Device


class MixinQuerys:
    def get_device_queryset(self) -> QuerySet:
        return Device.objects.all()
