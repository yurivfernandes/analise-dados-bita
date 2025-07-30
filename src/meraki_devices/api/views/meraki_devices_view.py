from rest_framework.viewsets import ModelViewSet

from app.utils.paginators import CustomLargePagination

from ...models import DeviceInventario
from ..filters import DeviceInventarioFilter
from ..serializers import DeviceSerializer

NAME_EXCLUDE = ["DANIFICADO", "Retirado"]


class MerakiDeviceView(ModelViewSet):
    serializer_class = DeviceSerializer
    queryset = DeviceInventario.objects.exclude(
        name__in=NAME_EXCLUDE
    ).order_by("id")
    pagination_class = CustomLargePagination
    filterset_class = DeviceInventarioFilter
