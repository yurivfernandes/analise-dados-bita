from rest_framework import serializers

from ...models import FIncidentTask


class IncidentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIncidentTask
        fields = "__all__"
