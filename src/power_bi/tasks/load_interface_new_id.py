from functools import cached_property

import polars as pl

# from celery import shared_task
from django.db import connection, models, transaction
from django.utils.functional import cached_property

from app.utils.pipeline import Pipeline

from ..models import SolarIDVGRInterfaceCorrigido, TblSolarInterfacesVgr
from ..utils.mixin import MixinViews


class LoadInterfaceNewID(MixinViews, Pipeline):
    """Extrai, transforma e carrega os dados de Receita Consolidados."""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.company_remedy_list = kwargs.get("company_remedy_list")
        self.nome_do_cliente_listt = kwargs.get("nome_do_cliente_list")

    def _get_solar_interface_vgr_queryset(self) -> models.QuerySet:
        """Retorna o queryset com as interfaces do solar"""
        return (
            TblSolarInterfacesVgr.objects.using("power_bi")
            .order_by("id")
            .filter(**self._filtro)
        )

    @cached_property
    def _filtro(self) -> dict:
        filtro = {}
        if self.company_remedy_list:
            filtro["company_remedy__in"] = self.company_remedy_list
        if self.nome_do_cliente_listt:
            filtro["nome_do_cliente__in"] = self.nome_do_cliente_listt
        return filtro

    @cached_property
    def schema(self) -> dict:
        """Busca o schema a ser utilizado no dataset"""
        return self.generate_schema_from_model(model=TblSolarInterfacesVgr)

    @property
    def solar_interface_dataset(self) -> pl.DataFrame:
        """Retorna um dataset com os dados de interfaces."""
        return self.get_dataset(
            query_set=self._get_solar_interface_vgr_queryset().values(
                *self.schema
            ),
            schema=self.schema,
        )

    def run(self) -> dict:
        self.extract_transform_dataset()
        self.load()
        return self.log

    def extract_transform_dataset(self) -> None:
        """Extrai e transforma o dataset principal incluindo log de IDs antigos."""
        self.dataset = (
            self.solar_interface_dataset.with_columns(
                pl.col("id_vgr").map_elements(
                    lambda x: x
                    if isinstance(x, str) and x.isdigit() and len(x) == 7
                    else None,
                    return_dtype=pl.String,
                )
            )
            .with_columns(
                pl.struct(["id_vgr", "status_vantive"])
                .map_elements(
                    lambda row: self.get_final_id_vgr(
                        row["id_vgr"], row["status_vantive"]
                    ),
                    return_dtype=pl.Struct,
                )
                .alias("novo_valores")
            )
            .with_columns(
                pl.col("novo_valores").struct.field("id_vgr").alias("id_vgr"),
                pl.col("novo_valores")
                .struct.field("status_vantive")
                .alias("status_vantive"),
                pl.col("novo_valores")
                .struct.field("historico_ids")
                .alias("historico_ids"),
            )
            .drop("novo_valores")
        )

    def get_final_id_vgr(self, id_vgr: str, status_vantive: str) -> dict:
        """Busca o ID final iterativamente e mantém um log de IDs."""
        historico_ids = [id_vgr]
        if id_vgr in (None, "N/A", "AMERICA TOWER - MTR-CORP-3226", "SPO-815"):
            return {
                "id_vgr": id_vgr,
                "status_vantive": status_vantive,
                "historico_ids": historico_ids,
            }

        if status_vantive in ("RFS Faturável", "RFS Técnico", "Cancelado"):
            return {
                "id_vgr": id_vgr,
                "status_vantive": status_vantive,
                "historico_ids": historico_ids,
            }

        while True:
            result = self.query_sae(id_vgr)
            novo_id = str(result["novo_id"])
            novo_status = result["status_vantive"]

            if novo_id in (None, "None", id_vgr):
                if status_vantive == novo_status:
                    return {
                        "id_vgr": id_vgr,
                        "status_vantive": status_vantive,
                        "historico_ids": historico_ids,
                    }
                return {
                    "id_vgr": id_vgr,
                    "status_vantive": novo_status,
                    "historico_ids": historico_ids,
                }

            elif novo_status in ("RFS Faturável", "RFS Técnico"):
                historico_ids.append(novo_id)
                return {
                    "id_vgr": novo_id,
                    "status_vantive": novo_status,
                    "historico_ids": historico_ids,
                }

            historico_ids.append(novo_id)
            id_vgr = novo_id

    def query_sae(self, id_vgr: str) -> dict:
        """Executa a query para buscar o novo ID e seu status e retorna um dicionário."""
        query = f"""
            WITH OrderedResults AS (
                SELECT  
                    ID_VANTIVE AS id_vgr,  
                    ID_VANTIVE_PRINCIPAL AS novo_id,  
                    STATUS_VANTIVE AS status_vantive,  
                    ROW_NUMBER() OVER (ORDER BY CASE WHEN STATUS_VANTIVE IS NOT NULL THEN 0 ELSE 1 END) AS rn
                FROM  
                OPENQUERY([10.128.223.125],  
                'SELECT *  
                FROM LK_RELATORIO_12.SAE.SAE.TB_PEDIDOS_DADOS WITH (NOLOCK)  
                WHERE ID_VANTIVE = ''{id_vgr}''')
            )
            SELECT id_vgr, novo_id, status_vantive
            FROM OrderedResults
            WHERE rn = 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        if result:
            return {
                "id_vgr": result[0],
                "status_vantive": result[2],
                "novo_id": result[1],
            }

        return {
            "id_vgr": id_vgr,
            "status_vantive": None,
            "novo_id": None,
        }

    @transaction.atomic
    def load(self) -> None:
        self._delete()
        self._save()

    def _delete(self):
        n_deleted, __ = (
            SolarIDVGRInterfaceCorrigido.objects.using("power_bi")
            .filter(**self._filtro)
            .delete()
        )
        self.log["n_deleted"] = n_deleted

    def _save(self):
        if self.dataset.is_empty():
            return

        objs = [
            SolarIDVGRInterfaceCorrigido(**vals)
            for vals in self.dataset.to_dicts()
        ]
        bulk = SolarIDVGRInterfaceCorrigido.objects.using(
            "power_bi"
        ).bulk_create(objs=objs, batch_size=1000)
        self.log["n_inserted"] = len(bulk)


# @shared_task(
#     name="receita.load_consolidacao",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_consolidacao_async(self, filtros: dict) -> dict:
    with LoadInterfaceNewID(**filtros) as task:
        log = task.run()
    return log
