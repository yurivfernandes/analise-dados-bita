from rest_framework import serializers

from ...models import FIncidentsBita


class FIncidentsBitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIncidentsBita
        fields = "__all__"  # Retorna todos os campos do model
