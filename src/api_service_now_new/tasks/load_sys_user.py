from typing import Dict, List

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import Incident, SysUser
from ..utils.servicenow import fetch_single_record, upsert_by_sys_id


def _chunked(seq: List[str], size: int = 100) -> List[List[str]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


class LoadSysUser(MixinGetDataset, Pipeline):
    """Carrega sys_user (users) do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        upsert_by_sys_id(dataset=self.dataset, model=SysUser, log=self.log)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._users

    @property
    def _users(self) -> pl.DataFrame:
        fields = ",".join([f.name for f in SysUser._meta.fields])

        # IDs únicos de usuários presentes em Incident (opened_by, resolved_by, closed_by)
        opened = (
            Incident.objects.exclude(opened_by__isnull=True)
            .exclude(opened_by="")
            .values_list("opened_by", flat=True)
            .distinct()
        )
        resolved = (
            Incident.objects.exclude(resolved_by__isnull=True)
            .exclude(resolved_by="")
            .values_list("resolved_by", flat=True)
            .distinct()
        )
        closed = (
            Incident.objects.exclude(closed_by__isnull=True)
            .exclude(closed_by="")
            .values_list("closed_by", flat=True)
            .distinct()
        )

        ids: List[str] = sorted({*opened, *resolved, *closed})

        if not ids:
            return pl.DataFrame(
                schema={f.name: pl.String for f in SysUser._meta.fields}
            )

        all_results: List[Dict] = []
        for sid in ids:
            rec = fetch_single_record(
                path="sys_user", sys_id=sid, params={"sysparm_fields": fields}
            )
            if rec:
                all_results.append(rec)

        if not all_results:
            return pl.DataFrame(
                schema={f.name: pl.String for f in SysUser._meta.fields}
            )

        return pl.DataFrame(
            all_results,
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
