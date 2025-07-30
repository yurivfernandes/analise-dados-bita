from datetime import datetime, timedelta
from typing import Dict

from celery import shared_task
from django.db import transaction
from django.db.models import Q

from service_now.models import Incident

from ..models import DCompany


class LoadDCompany:
    def __init__(self, update_all: bool = False):
        self.update_all = update_all
        self.log = {
            "total_created": 0,
            "total_updated": 0,
            "total_processed": 0,
        }
        self.company_data = None

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
        """Extrai os dados de company dos incidentes"""
        date_filter = Q()
        if not self.update_all:
            last_10_days = datetime.now() - timedelta(days=10)
            date_filter = Q(sys_updated_on__gte=last_10_days)

        self.company_data = (
            Incident.objects.filter(date_filter)
            .exclude(Q(company__isnull=True) | Q(dv_company__isnull=True))
            .values("company", "dv_company")
            .distinct()
        )
        self.log["total_processed"] = len(self.company_data)

    @transaction.atomic
    def load(self) -> None:
        """Carrega os dados no banco de dados"""
        if not self.company_data:
            return

        for item in self.company_data:
            company, created = DCompany.objects.update_or_create(
                id=item["company"],
                defaults={"dv_company": item["dv_company"]},
            )
            if created:
                self.log["total_created"] += 1
            else:
                self.log["total_updated"] += 1


@shared_task(
    name="dw_analytics.load_company",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_dcompany_async(self, update_all: bool = False) -> Dict:
    task = LoadDCompany(update_all=update_all)
    return task.run()
