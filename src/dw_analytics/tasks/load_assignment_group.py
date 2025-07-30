from datetime import datetime, timedelta
from typing import Dict

from celery import shared_task
from django.db import transaction
from django.db.models import Q

from service_now.models import Incident

from ..models import DAssignmentGroup


class LoadAssignmentGroup:
    def __init__(self, update_all: bool = False):
        self.update_all = update_all
        self.log = {
            "total_created": 0,
            "total_updated": 0,
            "total_processed": 0,
        }
        self.assignment_group_data = None

    def run(self) -> Dict:
        """Executa o processo completo de carregamento."""
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
        """Extrai os dados de assignment_group dos incidentes"""
        date_filter = Q()
        if not self.update_all:
            last_10_days = datetime.now() - timedelta(days=10)
            date_filter = Q(resolved_at__gte=last_10_days)

        self.assignment_group_data = (
            Incident.objects.filter(date_filter)
            .exclude(
                Q(assignment_group__isnull=True)
                | Q(assignment_group__exact="")
                | Q(assignment_group__exact=" ")
                | Q(dv_assignment_group__isnull=True)
                | Q(dv_assignment_group__exact="")
                | Q(dv_assignment_group__exact=" ")
            )
            .values(
                "assignment_group",
                "dv_assignment_group",
            )
            .distinct()
        )
        self.log["total_processed"] = len(self.assignment_group_data)

    @transaction.atomic
    def load(self) -> None:
        """Carrega os dados no banco de dados"""
        if not self.assignment_group_data:
            return

        # Limpa registros duplicados
        self._clean_duplicates()

        # Processa cada assignment_group
        for ag_data in self.assignment_group_data:
            assignment_group = DAssignmentGroup.objects.filter(
                dv_assignment_group=ag_data["dv_assignment_group"]
            ).first()

            if not assignment_group:
                DAssignmentGroup.objects.create(
                    dv_assignment_group=ag_data["dv_assignment_group"]
                )
                self.log["total_created"] += 1
            else:
                self.log["total_updated"] += 1

    def _clean_duplicates(self) -> None:
        """Remove registros duplicados mantendo o mais antigo"""
        for ag_data in self.assignment_group_data:
            duplicates = DAssignmentGroup.objects.filter(
                dv_assignment_group=ag_data["dv_assignment_group"]
            ).order_by("id")

            if duplicates.count() > 1:
                primary = duplicates.first()
                duplicates.exclude(id=primary.id).delete()


class LoadAssignmentGroupTask:
    """Classe para gerenciar o carregamento de assignment_group"""

    @staticmethod
    def execute(update_all=False):
        """
        Executa o carregamento dos dados de assignment_group

        Args:
            update_all (bool): Se True, busca todos os registros.
            Se False, busca apenas os últimos 10 dias.
        """
        try:
            task = LoadAssignmentGroup(update_all=update_all)
            return task.run()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao carregar assignment_group: {str(e)}",
            }


@shared_task(
    name="dw_analytics.load_assignment_group",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_assignment_group_async(self, update_all: bool = False) -> Dict:
    task = LoadAssignmentGroup(update_all=update_all)
    return task.run()
