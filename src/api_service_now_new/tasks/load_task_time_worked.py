from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import TaskTimeWorked
from ..utils.servicenow import paginate


class LoadTaskTimeWorked(MixinGetDataset, Pipeline):
    """Carrega task_time_worked do ServiceNow paginado."""

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        self.load(
            dataset=self.dataset, model=TaskTimeWorked, filtro=self._filtro
        )
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._task_time_worked

    @property
    def _task_time_worked(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in TaskTimeWorked._meta.fields])

        query = f"sys_created_on>={self.start_date} 00:00:00^sys_created_on<={self.end_date} 23:59:59"

        result_list = paginate(
            path="task_time_worked",
            params={"sysparm_fields": fields, "sysparm_query": query},
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in TaskTimeWorked._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_task_time_worked_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_task_time_worked_async(_task, start_date: str, end_date: str):
    sync_task = LoadTaskTimeWorked(start_date=start_date, end_date=end_date)
    return sync_task.run()
