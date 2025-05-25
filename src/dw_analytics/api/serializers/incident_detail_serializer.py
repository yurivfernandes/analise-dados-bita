from rest_framework import serializers

from ...models import FIncident
from .incident_task_serializer import IncidentTaskSerializer
from .planta_vgr_serializer import PlantaVgrSerializer
from .sae_localidades_serializer import SaeLocalidadesSerializer


class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class IncidentDetailSerializer(DynamicModelSerializer):
    incident_task = IncidentTaskSerializer(many=True, read_only=True)
    planta_vgr = PlantaVgrSerializer(read_only=True)
    sae_localidades = SaeLocalidadesSerializer(read_only=True)

    class Meta:
        model = FIncident
        fields = "__all__"
