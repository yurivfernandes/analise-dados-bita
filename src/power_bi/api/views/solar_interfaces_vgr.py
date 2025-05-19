from rest_framework.viewsets import ModelViewSet

from app.paginators import CustomLargePagination

from ...models import TblSolarInterfacesVgr
from ..serializers import SolarInterfacesVgrSerializer


class SolarInterfacesVGR(ModelViewSet):
    serializer_class = SolarInterfacesVgrSerializer
    queryset = TblSolarInterfacesVgr.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
