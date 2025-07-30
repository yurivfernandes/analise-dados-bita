from typing import Dict

import meraki
import polars as pl

from app.utils import MixinGetDataset, Pipeline

from ..models import Device


class LoadMerakiDevices(MixinGetDataset, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self, api_key: str):
        self.dashboard = meraki.DashboardAPI(
            api_key, suppress_logging=True, certificate_path=""
        )
        super().__init__()

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=Device, filtro={})
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = self._all_devices.fill_nan(None)

    @property
    def _organizations(self) -> list:
        """Retorna todas as organizações"""
        return self.dashboard.organizations.getOrganizations()

    @property
    def _all_devices(self) -> pl.DataFrame:
        """Busca todos os dispositivos de uma organização, paginando se necessário."""
        all_devices = []
        starting_after = None
        orgs = self._organizations
        dfs = []
        for org in orgs:
            org_id = org.get("id")
            while True:
                params = {"perPage": 1000}
                if starting_after:
                    params["startingAfter"] = starting_after
                resp = self.dashboard.organizations.getOrganizationDevices(
                    org_id, **params
                )
                if not resp:
                    break
                print(f"Org {org_id}: {len(resp)} dispositivos recebidos")
                all_devices.extend(resp)
                starting_after = resp[-1]["serial"]
                df_org = pl.DataFrame(data=all_devices)
            dfs.append(
                df_org.with_columns(pl.lit(org_id).alias("organization_id"))
            )

        return pl.concat(dfs)


# @shared_task(
#     name="dw_analytics.load_meraki_devices_async",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_meraki_devices_async(self, api_key: str = False) -> Dict:
    sync_task = LoadMerakiDevices(api_key=api_key)
    return sync_task.run()
