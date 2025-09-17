from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import Incident
from ..utils.servicenow import ensure_datetime, paginate


class LoadIncidentsOpened(MixinGetDataset, Pipeline):
    """Classe que busca incidents filtrando por `opened_at` no ServiceNow.

    Implementada no mesmo padrão da `LoadMerakiDevices`: utiliza uma `@property` que
    realiza a chamada paginada e `extract_and_transform_dataset` apenas atribui
    o resultado a `self.dataset`.
    """

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {"opened_at__range": [self.start_date, self.end_date]}

    def run(self) -> Dict:
        """Método principal: executa extração, persiste via `self.load` e retorna o log."""
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=Incident, filtro=self._filtro)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        """Preenche `self.dataset` a partir da property `_incidents` (polars DataFrame)."""
        self.dataset = self._incidents

    @property
    def _incidents(self) -> pl.DataFrame:
        """Retorna o dataset `polars.DataFrame` de incidents paginado do ServiceNow filtrado por opened_at."""
        start_ts = ensure_datetime(self.start_date, end=False)
        end_ts = ensure_datetime(self.end_date, end=True)

        # solicita apenas os campos presentes no model Incident
        fields = ",".join([f.name for f in Incident._meta.fields])

        query = f"opened_at>={start_ts}^opened_at<={end_ts}"
        params = {"sysparm_query": query, "sysparm_fields": fields}
        result_list = paginate(
            path="incident",
            params=params,
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )
        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in Incident._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_incidents_opened_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_incidents_opened_async(_task, start_date: str, end_date: str):
    sync_task = LoadIncidentsOpened(start_date=start_date, end_date=end_date)
    return sync_task.run()
