from rest_framework.viewsets import ModelViewSet

from app.utils.paginators import CustomLargePagination

from ...models import SolarIDVGRInterfaceCorrigido
from ..serializers import SolarInterfacesVgrSerializer


class SolarIDVGRInterfaceVGRCorrigido(ModelViewSet):
    serializer_class = SolarInterfacesVgrSerializer
    queryset = SolarIDVGRInterfaceCorrigido.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
