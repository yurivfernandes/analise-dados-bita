from django.db.models import QuerySet

from ..models import ContractSla


class MixinQuerys:
    def get_device_queryset(self) -> QuerySet:
        return ContractSla.objects.all()
