from rest_framework import serializers

from ...models import FPlantaVgr


class PlantaVgrSerializer(serializers.ModelSerializer):
    class Meta:
        model = FPlantaVgr
        fields = "__all__"
