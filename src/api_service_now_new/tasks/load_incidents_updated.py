from typing import Dict

import polars as pl
from celery import shared_task
from django.db import transaction

from api_service_now_new.models.incident import Incident
from api_service_now_new.utils.servicenow import ensure_datetime, paginate
from app.utils import MixinGetDataset, Pipeline


class LoadIncidentsUpdated(MixinGetDataset, Pipeline):
    """Classe que busca incidents filtrando por `sys_updated_on` no ServiceNow."""

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=Incident)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        """Preenche `self.dataset` a partir da property `_incidents` (polars DataFrame)."""
        self.dataset = self._incidents

    def load(self, dataset: pl.DataFrame, model) -> None:
        """Override: não faz delete+insert; apenas faz update dos registros por `sys_id`."""
        self.log.setdefault("n_updated", 0)
        self._update(dataset=dataset, model=model)

    @transaction.atomic
    def _update(self, dataset: pl.DataFrame, model) -> None:
        """Atualiza registros existentes por `sys_id` a partir do dataset usando bulk_update.

        Estratégia:
        - Extrair sys_ids do dataset
        - Buscar as instâncias existentes em um único query
        - Atualizar atributos em memória e usar `bulk_update`
        """
        if dataset.is_empty():
            return

        rows = dataset.to_dicts()
        sys_ids = [r.get("sys_id") for r in rows if r.get("sys_id")]
        if not sys_ids:
            self.log["n_updated"] = 0
            return

        # buscar instâncias existentes
        existing_qs = model.objects.filter(sys_id__in=sys_ids)
        existing_map = {getattr(obj, "sys_id"): obj for obj in existing_qs}

        # campos do model a serem atualizados (exclui pk e sys_id)
        updatable_fields = [
            f.name
            for f in model._meta.fields
            if not getattr(f, "auto_created", False) and f.name != "sys_id"
        ]

        instances_to_update = []
        for row in rows:
            sid = row.get("sys_id")
            inst = existing_map.get(sid)
            if not inst:
                continue
            for k, v in row.items():
                if k in updatable_fields:
                    setattr(inst, k, v)
            instances_to_update.append(inst)

        if instances_to_update:
            model.objects.bulk_update(
                instances_to_update, fields=updatable_fields, batch_size=1000
            )

        self.log["n_updated"] = len(instances_to_update)

    @property
    def _incidents(self) -> pl.DataFrame:
        start_ts = ensure_datetime(self.start_date, end=False)
        end_ts = ensure_datetime(self.end_date, end=True)

        # solicita apenas os campos presentes no model Incident
        fields = ",".join([f.name for f in Incident._meta.fields])

        query = f"sys_updated_on>={start_ts}^sys_updated_on<={end_ts}"
        params = {"sysparm_query": query, "sysparm_fields": fields}
        return paginate(
            path="incident",
            params=params,
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )


@shared_task(
    name="api_service_now_new.load_incidents_updated_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_incidents_updated_async(_task, start_date: str, end_date: str):
    sync_task = LoadIncidentsUpdated(start_date=start_date, end_date=end_date)
    return sync_task.run()
