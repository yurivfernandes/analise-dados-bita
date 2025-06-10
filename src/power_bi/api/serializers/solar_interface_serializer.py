from rest_framework import serializers

from ...models import SolarInterface


class SolarInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarInterface
        fields = "__all__"  # Retorna todos os campos do model
