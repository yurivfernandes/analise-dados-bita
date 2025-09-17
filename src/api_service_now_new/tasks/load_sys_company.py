from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import SysCompany
from ..utils.servicenow import paginate, upsert_by_sys_id


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

        result_list = paginate(
            path="sys_company",
            params={"sysparm_fields": fields},
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in SysCompany._meta.fields},
        )

    # ...existing code...


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
