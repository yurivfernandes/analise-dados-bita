from typing import Dict, List

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import Incident, SysUser
from ..utils.servicenow import paginate, upsert_by_sys_id


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
        for chunk in _chunked(ids, size=100):
            query = f"sys_idIN{','.join(chunk)}"
            batch = paginate(
                path="sys_user",
                params={"sysparm_fields": fields, "sysparm_query": query},
                limit=10000,
                mode="offset",
                limit_param="sysparm_limit",
                offset_param="sysparm_offset",
                result_key="result",
            )
            if isinstance(batch, list):
                all_results.extend(batch)
            else:
                all_results.extend(pl.DataFrame(batch).to_dicts())

        return pl.DataFrame(all_results).select(
            [f.name for f in SysUser._meta.fields]
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
