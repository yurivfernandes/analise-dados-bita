from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import SysUser
from ..utils.servicenow import paginate


class LoadSysUser(MixinGetDataset, Pipeline):
    """Carrega sys_user (users) do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=SysUser, filtro=self._filtro)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._users

    @property
    def _users(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in SysUser._meta.fields])

        result_list = paginate(
            path="sys_user",
            params={"sysparm_fields": fields},
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in SysUser._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_sys_user_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_sys_user_async(_task):
    sync_task = LoadSysUser()
    return sync_task.run()
