from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import CmdbCiNetworkLink
from ..utils.servicenow import paginate, upsert_by_sys_id


class LoadCmdbCiNetworkLink(MixinGetDataset, Pipeline):
    """Carrega itens de CMDB (cmdb_ci_network_link) do ServiceNow paginado."""

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        upsert_by_sys_id(
            dataset=self.dataset, model=CmdbCiNetworkLink, log=self.log
        )
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._dataset

    @property
    def _dataset(self) -> pl.DataFrame:
        fields = ",".join(
            [
                f.name
                for f in CmdbCiNetworkLink._meta.fields
                if not f.name.startswith("etl_") and f.name != "etl_hash"
            ]
        )

        # aplicar filtro por assignment_group (fila) similar aos loaders de incidents
        query = ""
        add_q = "assignment_groupLIKEvita"
        if add_q:
            query = add_q

        params = {"sysparm_fields": fields}
        if query:
            params["sysparm_query"] = query

        result_list = paginate(
            path="cmdb_ci_network_link",
            params=params,
            limit=5000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in CmdbCiNetworkLink._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_cmdb_ci_network_link_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_cmdb_ci_network_link_async(_task):
    sync_task = LoadCmdbCiNetworkLink()
    return sync_task.run()
