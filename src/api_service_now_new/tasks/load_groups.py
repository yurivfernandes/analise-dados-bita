from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import Groups
from ..utils.servicenow import paginate, upsert_by_sys_id


class LoadGroups(MixinGetDataset, Pipeline):
    """Carrega sys_user_group (groups) do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        # usar utilitário genérico de upsert por sys_id
        upsert_by_sys_id(dataset=self.dataset, model=Groups, log=self.log)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._groups

    @property
    def _groups(self) -> pl.DataFrame:
        fields = ",".join(
            [
                f.name
                for f in Groups._meta.fields
                if not f.name.startswith("etl_") and f.name != "etl_hash"
            ]
        )

        params = {
            "sysparm_fields": fields,
            "sysparm_query": "nameSTARTSWITHvita^ORnameSTARTSWITHvivo b2b centro servi",
        }

        result_list = paginate(
            path="sys_user_group",
            params=params,
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in Groups._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_groups_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_groups_async(_task):
    sync_task = LoadGroups()
    return sync_task.run()
