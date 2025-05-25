from rest_framework import serializers


class FieldMetadataSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    verbose_name = serializers.CharField()
    is_relation = serializers.BooleanField()
    related_model = serializers.CharField(allow_null=True)
    related_fields = serializers.ListField(
        child=serializers.CharField(), allow_null=True
    )
