from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.utils.paginators import CustomPagination

from ..filters import IncidentFilterService
from ..serializers import IncidentDetailSerializer


class IncidentViewSet(ModelViewSet):
    serializer_class = IncidentDetailSerializer
    pagination_class = CustomPagination
    ordering_fields = [
        "number",
        "opened_at",
        "closed_at",
        "company",
        "assignment_group",
    ]
    ordering = ["-opened_at"]  # ordenação padrão

    def get_queryset(self):
        filter_service = IncidentFilterService(self.request.query_params)
        return filter_service.get_queryset()

    def get_serializer(self, *args, **kwargs):
        kwargs["fields"] = self.request.query_params.getlist("fields", None)

        # Configura campos para relações
        for relation in ["incident_task", "planta_vgr", "sae_localidades"]:
            relation_fields = self.request.query_params.getlist(
                f"{relation}_fields", None
            )
            if relation_fields:
                kwargs[f"{relation}_fields"] = relation_fields

        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
