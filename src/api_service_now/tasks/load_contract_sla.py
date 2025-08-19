from typing import Dict

import polars as pl
import requests
from celery import shared_task
from dotenv import load_dotenv

from app.utils import MixinGetDataset, Pipeline

from ..models import ContractSla

load_dotenv()

PATH_CONTRACT_SLA = "/contract_sla"


class LoadContractSLA(Pipeline, MixinGetDataset):
    def __init__(self, params: dict):
        self.base_url = params.get("service_now_base_url")
        self.auth = (
            params.get("service_now_username"),
            params.get("service_now_user_password"),
        )
        self.headers = {"Content-Type": "application/json"}
        super().__init__()

    def run(self) -> dict:
        dataset = self._contract_sla_dataset
        self.load(dataset=dataset, model=ContractSla, filtro={})
        return self.log

    @property
    def _contract_sla_dataset(self) -> pl.DataFrame:
        url = f"{self.base_url}{PATH_CONTRACT_SLA}"
        params = {"sysparm_limit": 10000}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        clean_data = [
            {
                key: value.get("value") if isinstance(value, dict) else value
                for key, value in item.items()
            }
            for item in response.json().get("result", [])
        ]
        schema = self.generate_schema_from_model(model=ContractSla)
        return pl.DataFrame(
            data=clean_data,
            schema={k: v["type"] for k, v in schema.items() if k != 'id'},
            infer_schema_length=1000,
        ).rename({k: v["rename"] for k, v in schema.items()})


@shared_task(
    name="meraki.load_meraki_devices_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_meraki_devices_async(self, params: dict) -> Dict:
    sync_task = LoadContractSLA(params=params)
    return sync_task.run()
