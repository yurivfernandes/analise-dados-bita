from rest_framework import serializers

from ...models import SolarIDVGRInterfaceCorrigido


class SolarIDVGRInterfaceCorrigidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarIDVGRInterfaceCorrigido
        fields = "__all__"  # Retorna todos os campos do model
