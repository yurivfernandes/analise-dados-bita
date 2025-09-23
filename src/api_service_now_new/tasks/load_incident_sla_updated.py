from typing import Dict

import polars as pl
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from app.utils import MixinGetDataset, Pipeline

from ..models import IncidentSla
from ..utils.servicenow import ensure_datetime, paginate


class LoadIncidentSlaUpdated(MixinGetDataset, Pipeline):
    """Carrega incident_sla do ServiceNow e atualiza registros existentes por sys_id."""

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    def run(self) -> Dict:
        started = timezone.now()
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=IncidentSla)
        finished = timezone.now()
        run_duration = round((finished - started).total_seconds(), 2)
        self.log["run_duration"] = run_duration
        print(f"...RUN DURATION: {run_duration}s...")
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._incident_sla

    def load(self, dataset: pl.DataFrame, model) -> None:
        self.log.setdefault("n_updated", 0)
        self._update(dataset=dataset, model=model)

    @transaction.atomic
    def _update(self, dataset: pl.DataFrame, model) -> None:
        if dataset.is_empty():
            self.log["n_updated"] = 0
            self.log.setdefault("update_duration", 0.0)
            return

        rows = dataset.to_dicts()
        sys_ids = [r.get("sys_id") for r in rows if r.get("sys_id")]
        if not sys_ids:
            self.log["n_updated"] = 0
            return

        existing_qs = model.objects.filter(sys_id__in=sys_ids)
        existing_map = {getattr(obj, "sys_id"): obj for obj in existing_qs}

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

        started = timezone.now()
        if instances_to_update:
            model.objects.bulk_update(
                instances_to_update, fields=updatable_fields, batch_size=1000
            )
        finished = timezone.now()
        duration = round((finished - started).total_seconds(), 2)
        self.log["n_updated"] = len(instances_to_update)
        self.log["update_duration"] = duration
        print(
            f"...{len(instances_to_update)} REGISTROS ATUALIZADOS NO BANCO DE DADOS..."
        )
        print(f"...UPDATE DURATION: {duration}s...")

    @property
    def _incident_sla(self) -> pl.DataFrame:
        start_ts = ensure_datetime(self.start_date, end=False)
        end_ts = ensure_datetime(self.end_date, end=True)

        fields = ",".join(
            [
                f.name
                for f in IncidentSla._meta.fields
                if not f.name.startswith("etl_") and f.name != "etl_hash"
            ]
        )

        query = f"sys_created_on>={start_ts}^sys_created_on<={end_ts}^taskISNOTEMPTY^task.assignment_group.nameSTARTSWITHvita"
        params = {"sysparm_fields": fields, "sysparm_query": query}
        result_list = paginate(
            path="task_sla",
            params=params,
            limit=10000,
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
    name="api_service_now_new.load_incident_sla_updated_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_incident_sla_updated_async(_task, start_date: str, end_date: str):
    sync_task = LoadIncidentSlaUpdated(
        start_date=start_date, end_date=end_date
    )
    return sync_task.run()
