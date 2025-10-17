from django.db.models import QuerySet

from ..models import ContractSla, Incident, IncidentSla


class MixinQuerys:
    """Fornece QuerySets base (sem filtros) para uso nas tasks."""

    def get_incident_queryset(self) -> QuerySet:
        return Incident.objects.all()

    def get_incident_sla_queryset(self) -> QuerySet:
        return IncidentSla.objects.all()

    def get_contract_sla_queryset(self) -> QuerySet:
        return ContractSla.objects.all()
