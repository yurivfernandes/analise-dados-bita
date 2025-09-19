from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import IncidentSla
from ..utils.servicenow import ensure_datetime, paginate


class LoadIncidentSla(MixinGetDataset, Pipeline):
    """Carrega incident_sla do ServiceNow paginado."""

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {
            "sys_created_on__gte": ensure_datetime(self.start_date, end=False),
            "sys_created_on__lte": ensure_datetime(self.end_date, end=True),
        }

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=IncidentSla, filtro=self._filtro)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._incident_sla

    @property
    def _incident_sla(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in IncidentSla._meta.fields])
        query = f"sys_created_on>={self.start_date} 00:00:00^sys_created_on<={self.end_date} 23:59:59^taskISNOTEMPTY"
        # para task_sla o assignment_group pertence ao task referenciado -> usar dot-walk
        add_q = "task.assignment_group.nameLIKEvita"
        if add_q not in query:
            query = f"{query}^{add_q}"
        result_list = paginate(
            path="task_sla",
            params={"sysparm_fields": fields, "sysparm_query": query},
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in IncidentSla._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_incident_sla_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_incident_sla_async(_task, start_date: str, end_date: str):
    sync_task = LoadIncidentSla(start_date=start_date, end_date=end_date)
    return sync_task.run()
