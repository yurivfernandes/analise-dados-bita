from rest_framework import serializers

from ...models import FSaeLocalidades


class SaeLocalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FSaeLocalidades
        fields = "__all__"
