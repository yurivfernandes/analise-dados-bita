from rest_framework.viewsets import ModelViewSet

from app.utils.paginators import CustomLargePagination

from ...models import SolarIDVGRInterfaceCorrigido
from ..serializers import SolarIDVGRInterfaceCorrigidoSerializer


class SolarIDVGRInterfaceVGRCorrigido(ModelViewSet):
    serializer_class = SolarIDVGRInterfaceCorrigidoSerializer
    queryset = SolarIDVGRInterfaceCorrigido.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
