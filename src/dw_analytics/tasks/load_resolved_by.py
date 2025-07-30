from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

from celery import shared_task
from django.db import transaction
from django.db.models import Q, QuerySet

from service_now.models import Incident

from ..utils import MixinQuerys


class LoadResolvedBy(MixinQuerys):
    def __init__(self, update_all: bool = False):
        self.update_all = update_all
        self.log = {
            "total_created": 0,
            "total_updated": 0,
            "total_processed": 0,
        }
        self.resolved_by_data = None

    def run(self) -> Dict:
        """Executa o processo completo de carregamento"""
        self.extract_data()
        self.load()
        return {
            "status": "success",
            "message": (
                f"Dados atualizados com sucesso. "
                f"Criados: {self.log['total_created']}, "
                f"Atualizados: {self.log['total_updated']}, "
                f"Processados: {self.log['total_processed']}"
            ),
        }

    def extract_data(self) -> None:
        """Extrai os dados de resolved_by dos incidentes"""
        date_filter = Q()
        if not self.update_all:
            last_10_days = datetime.now() - timedelta(days=10)
            date_filter = Q(resolved_at__gte=last_10_days)

        self.resolved_by_data = (
            Incident.objects.filter(date_filter)
            .exclude(
                Q(resolved_by__isnull=True)
                | Q(dv_resolved_by__isnull=True)
                | Q(assignment_group__isnull=True)
                | Q(dv_assignment_group__isnull=True)
            )
            .values(
                "resolved_by",
                "dv_resolved_by",
                "assignment_group",
                "dv_assignment_group",
            )
            .distinct()
        )
        self.log["total_processed"] = len(self.resolved_by_data)

    @cached_property
    def _resolved_by(self) -> QuerySet:
        return self.get_resolved_by_queryset()

    @cached_property
    def _assignment_group(self) -> QuerySet:
        return self.get_assignment_group_queryset()

    @transaction.atomic
    def load(self) -> None:
        """Carrega os dados no banco de dados"""
        if not self.resolved_by_data:
            return

        self._clean_duplicates()

        resolved_by_groups = {}
        for item in self.resolved_by_data:
            rb_name = item["dv_resolved_by"]
            if rb_name not in resolved_by_groups:
                resolved_by_groups[rb_name] = {
                    "groups": set(),
                    "dv_groups": set(),
                }
            resolved_by_groups[rb_name]["groups"].add(item["assignment_group"])
            resolved_by_groups[rb_name]["dv_groups"].add(
                item["dv_assignment_group"]
            )

        for rb_name, data in resolved_by_groups.items():
            resolved_by = self._resolved_by.filter(
                dv_resolved_by=rb_name
            ).first()

            if not resolved_by:
                resolved_by = self._resolved_by.create(dv_resolved_by=rb_name)
                self.log["total_created"] += 1
            else:
                self.log["total_updated"] += 1

            assignment_groups = self._assignment_group.filter(
                dv_assignment_group__in=data["dv_groups"]
            )

            current_groups = set(
                resolved_by.assignment_group.values_list(
                    "dv_assignment_group", flat=True
                )
            )
            new_groups = set(
                ag.dv_assignment_group for ag in assignment_groups
            )
            groups_to_add = new_groups - current_groups

            if groups_to_add:
                groups_to_add_ids = self._assignment_group.filter(
                    dv_assignment_group__in=groups_to_add
                ).values_list("id", flat=True)
                resolved_by.assignment_group.add(*groups_to_add_ids)

    def _clean_duplicates(self) -> None:
        """Remove registros duplicados mantendo o mais antigo"""
        for rb_data in self.resolved_by_data:
            duplicates = (
                self.get_resolved_by_queryset()
                .filter(dv_resolved_by=rb_data["dv_resolved_by"])
                .order_by("id")
            )

            if duplicates.count() > 1:
                primary = duplicates.first()
                duplicates.exclude(id=primary.id).delete()


@shared_task(
    name="dw_analytics.load_resolved_by",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_resolved_by_async(self, update_all: bool = False) -> Dict:
    task = LoadResolvedBy(update_all=update_all)
    return task.run()
