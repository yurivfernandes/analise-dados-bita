from rest_framework.viewsets import ModelViewSet

from app.paginators import CustomLargePagination

from ...models import FIncidentsBita
from ..serializers import FIncidentsBitaSerializer


class FIncidentsBitaViewset(ModelViewSet):
    serializer_class = FIncidentsBitaSerializer
    queryset = FIncidentsBita.objects.using("dw_analytics").all()
    pagination_class = CustomLargePagination
