from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import FIncident
from ..serializers import FieldMetadataSerializer


class FIncidentFieldsView(APIView):
    def get(self, request):
        fields_metadata = []
        model = FIncident

        for field in model._meta.get_fields():
            field_data = {
                "name": field.name,
                "type": field.get_internal_type(),
                "verbose_name": getattr(field, "verbose_name", field.name),
                "is_relation": isinstance(field, models.ForeignKey),
                "related_model": None,
                "related_fields": None,
            }

            if field_data["is_relation"]:
                related_model = field.related_model
                field_data["related_model"] = related_model._meta.model_name
                field_data["related_fields"] = [
                    f.name
                    for f in related_model._meta.fields
                    if not f.name.startswith("_")
                ]

            fields_metadata.append(field_data)

        serializer = FieldMetadataSerializer(fields_metadata, many=True)
        return Response(serializer.data)
