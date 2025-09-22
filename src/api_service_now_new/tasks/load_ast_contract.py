from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import AstContract
from ..utils.servicenow import paginate, upsert_by_sys_id


class LoadAstContract(MixinGetDataset, Pipeline):
    """Carrega ast_contract do ServiceNow paginado.

    Padrão semelhante a `LoadContractSla`: propriedade que realiza
    a chamada paginada e `extract_and_transform_dataset` atribui a
    `self.dataset`.
    """

    def __init__(self):
        super().__init__()

    @property
    def _filtro(self) -> dict:
        return {}

    def run(self) -> Dict:
        self.extract_and_transform_dataset()
        upsert_by_sys_id(dataset=self.dataset, model=AstContract, log=self.log)
        return self.log

    def extract_and_transform_dataset(self) -> None:
        self.dataset = self._ast_contract

    @property
    def _ast_contract(self) -> pl.DataFrame:
        fields = ",".join(
            [
                f.name
                for f in AstContract._meta.fields
                if not f.name.startswith("etl_") and f.name != "etl_hash"
            ]
        )

        # Buscar todos os contratos ativos ou todos dependendo da necessidade
        # Por enquanto, sem filtros específicos - pode ser ajustado conforme necessário
        params = {"sysparm_fields": fields}

        result_list = paginate(
            path="ast_contract",
            params=params,
            limit=10000,
            mode="offset",
            limit_param="sysparm_limit",
            offset_param="sysparm_offset",
            result_key="result",
        )

        return pl.DataFrame(
            result_list,
            schema={f.name: pl.String for f in AstContract._meta.fields},
        )


@shared_task(
    name="api_service_now_new.load_ast_contract_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_ast_contract_async(_task):
    sync_task = LoadAstContract()
    return sync_task.run()
