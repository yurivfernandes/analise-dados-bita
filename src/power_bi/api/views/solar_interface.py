from rest_framework.viewsets import ModelViewSet

from app.utils.paginators import CustomLargePagination

from ...models import SolarInterface
from ..serializers import SolarInterfaceSerializer


class SolarInterface(ModelViewSet):
    serializer_class = SolarInterfaceSerializer
    queryset = SolarInterface.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
