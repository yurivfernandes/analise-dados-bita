from django.db.models import Prefetch, Q

from ...models import FIncident, FIncidentTask, FPlantaVgr, FSaeLocalidades


class IncidentFilterService:
    RELATED_MODELS = {
        "incident_task": {
            "model": FIncidentTask,
            "join_fields": ("sys_id", "incident"),
        },
        "planta_vgr": {
            "model": FPlantaVgr,
            "join_fields": ("u_id_vgr", "id_vantive"),
        },
        "sae_localidades": {
            "model": FSaeLocalidades,
            "join_fields": ("u_id_vgr", "id_vantive"),
        },
    }

    def __init__(self, query_params):
        self.query_params = query_params
        self.include_relations = query_params.getlist("include_relations", [])
        self.selected_fields = query_params.getlist("fields", [])
        self.related_fields = {
            relation: query_params.getlist(f"{relation}_fields", [])
            for relation in self.include_relations
        }
        self.ordering = query_params.get("ordering", "-opened_at")

    def build_filters(self):
        filters = Q()
        exclude_params = ["page", "page_size", "include_relations"]

        for key, value in self.query_params.items():
            if key not in exclude_params and value:
                if (
                    "__" in key
                ):  # Filtros com lookups específicos (ex: date__gte)
                    filters &= Q(**{key: value})
                else:
                    filters &= Q(**{f"{key}__icontains": value})

        return filters

    def get_queryset(self):
        queryset = FIncident.objects.all()

        if self.selected_fields:
            # Garante que o ID sempre esteja presente
            if "id" not in self.selected_fields:
                self.selected_fields.append("id")
            queryset = queryset.only(*self.selected_fields)

        filters = self.build_filters()
        if filters:
            queryset = queryset.filter(filters)

        # Adiciona os relacionamentos
        if self.include_relations:
            for relation in self.include_relations:
                if relation in self.RELATED_MODELS:
                    if self.related_fields.get(relation):
                        # Se campos específicos foram solicitados para esta relação
                        queryset = queryset.prefetch_related(
                            Prefetch(
                                relation,
                                queryset=self.RELATED_MODELS[relation][
                                    "model"
                                ].objects.only(*self.related_fields[relation]),
                            )
                        )
                    else:
                        queryset = queryset.prefetch_related(relation)

        # Aplica ordenação
        if self.ordering:
            ordering_fields = self.ordering.split(",")
            queryset = queryset.order_by(*ordering_fields)

        return queryset
