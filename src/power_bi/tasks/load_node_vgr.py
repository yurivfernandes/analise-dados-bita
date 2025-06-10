import polars as pl

from app.utils.pipeline import Pipeline

from ..models import SolarNode
from ..utils import MixinTasksSolar

# from celery import shared_task


class LoadNodeVGR(MixinTasksSolar, Pipeline):
    """Extrai, transforma e carrega os dados de nodes."""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.company_remedy_list = kwargs.get("company_remedy_list")
        self.nome_cliente_list = kwargs.get("nome_cliente_list")

    @property
    def _filtro(self) -> dict:
        if (
            len(self.company_remedy_list) > 0
            and len(self.nome_cliente_list) > 0
        ):
            return {
                "company_remedy__in": self.company_remedy_list,
                "nome_cliente__in": self.nome_cliente_list,
            }
        if len(self.company_remedy_list) > 0:
            return {"company_remedy__in": self.company_remedy_list}
        if len(self.nome_cliente_list) > 0:
            return {
                "nome_cliente__in": self.nome_cliente_list,
            }
        return {}

    def run(self) -> dict:
        print(f"...INICIANDO A TASK [{self.__class__.__name__}]...")
        dataset = self.transform_dataset(dataset=self.solar_node_original)
        print("...DATASET PRONTO PARA SER INSERIDO NO BANCO!...")
        self.load(dataset=dataset, model=SolarNode)
        print("...DADOS SALVOS NO BANCO, FINALIZANDO...")
        return self.log

    def corrigir_operadoras(self, df: pl.DataFrame) -> pl.DataFrame:
        """Corrige o nome das operadores conforme a tabela [SolarNomeOperadoraCorreto] e tenta buscar o nome da operadora em outras colunas."""
        print("...BUSCANDO E CORRIGINDO OS NOMES DE OPERADORAS...")
        return (
            df.join(self.nome_operadora_correto, how="left", on="operadora")
            .with_columns(
                pl.when(pl.col("nome_correto").is_null())
                .then(pl.col("operadora"))
                .otherwise(pl.col("nome_correto"))
                .alias("operadora")
            )
            .drop("nome_correto")
            .with_columns(
                pl.when(
                    pl.col("operadora").is_in(
                        [None, "N/A", "Null", "null", "None", "n/a"]
                    )
                )
                .then(
                    pl.col("caption").map_elements(
                        self.encontrar_operadora, return_dtype=str | None
                    )
                )
                .otherwise(pl.col("operadora"))
                .alias("operadora")
            )
        )

    def selecionar_colunas(self, df: pl.DataFrame) -> pl.DataFrame:
        return df.select(
            [
                "node_id",
                "company_remedy",
                "nome_cliente",
                "razao_social",
                "grupo_corporativo",
                "id_vgr",
                "designador",
                "operadora",
                "tecnologia",
                "municipio",
                "uf",
                "status_vantive",
                "velocidade",
                "ip_node",
                "historico_ids",
            ]
        )


# @shared_task(
#     name="receita.load_consolidacao",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_node_vgr_async(self, filtros: dict) -> dict:
    with LoadNodeVGR(**filtros) as task:
        log = task.run()
    return log
