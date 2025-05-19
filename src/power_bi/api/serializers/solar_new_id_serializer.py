from rest_framework import serializers

from ...models import TblSolarInterfacesVgr


class SolarInterfacesVgrSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSolarInterfacesVgr
        fields = "__all__"  # Retorna todos os campos do model
