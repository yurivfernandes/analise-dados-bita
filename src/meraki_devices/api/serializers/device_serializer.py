from rest_framework import serializers

from ...models import DeviceInventario


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInventario
        fields = "__all__"
