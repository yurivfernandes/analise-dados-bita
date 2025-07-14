from django.db.models import QuerySet

from service_now.models import Incident, IncidentSLA

from ..models import (
    DAssignmentGroup,
    DCompany,
    DContract,
    DPremissa,
    DResolvedBy,
    DSortedTicket,
    FIncident,
)


class MixinQuerys:
    def get_resolved_by_queryset(self) -> QuerySet:
        return DResolvedBy.objects.all()

    def get_assignment_group_queryset(self) -> QuerySet:
        return DAssignmentGroup.objects.all()

    def get_company_queryset(self) -> QuerySet:
        return DCompany.objects.all()

    def get_contract_queryset(self) -> QuerySet:
        return DContract.objects.all()

    def get_sorted_ticket_queryset(self) -> QuerySet:
        return DSortedTicket.objects.all()

    def get_f_incident_queryset(self) -> QuerySet:
        return FIncident.objects.all()

    def get_premissa_queryset(self) -> QuerySet:
        return DPremissa.objects.all().select_related("assignment_group")

    def get_incident_queryset(self) -> QuerySet:
        return Incident.objects.all()

    def get_incident_sla_queryset(self) -> QuerySet:
        return IncidentSLA.objects.all()
