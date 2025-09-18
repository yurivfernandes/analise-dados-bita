from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import CmdbCi
from ..utils.servicenow import paginate, upsert_by_sys_id


class LoadCmdbCi(MixinGetDataset, Pipeline):
    """Carrega itens de CMDB (cmdb_ci) do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        upsert_by_sys_id(dataset=self.dataset, model=CmdbCi, log=self.log)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._cmdb_ci

    @property
    def _cmdb_ci(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in CmdbCi._meta.fields])

        result_list = paginate(
            path="cmdb_ci",
            params={"sysparm_fields": fields},
            limit=5000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in CmdbCi._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_cmdb_ci_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_cmdb_ci_async(_task):
    sync_task = LoadCmdbCi()
    return sync_task.run()
