from typing import Dict, List

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import Incident, SysCompany
from ..utils.servicenow import fetch_single_record, upsert_by_sys_id


def _chunked(seq: List[str], size: int = 100) -> List[List[str]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


class LoadSysCompany(MixinGetDataset, Pipeline):
    """Carrega sys_company do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        upsert_by_sys_id(dataset=self.dataset, model=SysCompany, log=self.log)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._companies

    @property
    def _companies(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in SysCompany._meta.fields])

        # IDs únicos de companies presentes em Incident
        qs = (
            Incident.objects.exclude(company__isnull=True)
            .exclude(company="")
            .values_list("company", flat=True)
            .distinct()
        )
        ids = sorted({x for x in qs if x})

        if not ids:
            # retorna DF vazio com schema correto
            return pl.DataFrame(
                schema={f.name: pl.String for f in SysCompany._meta.fields}
            )

        all_results: List[Dict] = []
        # agora chamamos a API uma vez por sys_id
        for sid in ids:
            rec = fetch_single_record(path="sys_company", sys_id=sid, params={"sysparm_fields": fields})
            if rec:
                all_results.append(rec)

        if not all_results:
            return pl.DataFrame(
                schema={f.name: pl.String for f in SysCompany._meta.fields}
            )

        return pl.DataFrame(all_results).select(
            [f.name for f in SysCompany._meta.fields]
        )


@shared_task(
    name="api_service_now_new.load_sys_company_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_sys_company_async(_task):
    sync_task = LoadSysCompany()
    return sync_task.run()
