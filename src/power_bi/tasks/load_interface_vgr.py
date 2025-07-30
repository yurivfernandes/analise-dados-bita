import polars as pl
from celery import shared_task

from app.utils.pipeline import Pipeline

from ..models import SolarInterface, SolarInterfaceOriginal
from ..utils import MixinETLSolar


class LoadInterfaceVGR(Pipeline, MixinETLSolar):
    """Extrai, transforma e carrega os dados de Interfaces."""

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
        self.dataset = self.solar_interface_original
        lenght_dataset_inicial = len(self.dataset)
        self.transform_dataset()
        lenght_dataset_final = len(self.dataset)
        if lenght_dataset_inicial != lenght_dataset_final:
            raise Exception(
                "O tamanho do dataset inicial é diferente do dataset final. "
                "Procure o suporte para analisar o problema."
            )
        print("...DATASET PRONTO PARA SER INSERIDO NO BANCO!...")
        self.load(
            dataset=self.dataset, model=SolarInterface, filtro=self._filtro
        )
        print("...FINALIZANDO A PIPELINE...")
        return self.log

    @property
    def solar_interface_original(self) -> pl.DataFrame:
        """Retorna os registros as interfaces que foram importadas do solar."""
        print("...BUSCANDO OS DADOS DAS INTERFACES...")
        schema = self.generate_schema_from_model(model=SolarInterfaceOriginal)
        return self.get_dataset(
            query_set=self.get_solar_interface_original_queryset().values(
                *schema
            ),
            schema=schema,
        )

    def transform_dataset(self) -> None:
        """Extrai e transforma o dataset principal incluindo log de IDs antigos."""
        self.dataset = (
            self.dataset.pipe(self.limpar_texto)
            .pipe(self.corrigir_operadoras)
            .pipe(self.corrigir_tecnologias)
            .pipe(self.corrigir_nome_cliente)
            .pipe(self.get_uf_and_municipio)
            .pipe(self.get_novo_id_vgr)
            .pipe(self.selecionar_colunas)
        )

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
                    pl.col("interface_name").map_elements(
                        self.encontrar_operadora, return_dtype=str | None
                    )
                )
                .otherwise(pl.col("operadora"))
                .alias("operadora")
            )
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
            .with_columns(
                pl.when(
                    pl.col("operadora").is_in(
                        [None, "N/A", "Null", "null", "None", "n/a"]
                    )
                )
                .then(
                    pl.col("nome_interface").map_elements(
                        self.encontrar_operadora, return_dtype=str | None
                    )
                )
                .otherwise(pl.col("operadora"))
                .alias("operadora")
            )
        )

    def selecionar_colunas(self, df: pl.DataFrame) -> pl.DataFrame:
        """Seleciona as colunas do dataset de acordo com as colunas a serem salvas no banco"""
        return df.select(
            [
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
                "velocidade",
                "status_vantive",
                "interface_id",
                "ip_interface",
                "ip_node",
                "historico_ids",
            ]
        )


@shared_task(
    name="power_bi.load_interface_vgr",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_interface_vgr_async(self, filtros: dict) -> dict:
    with LoadInterfaceVGR(**filtros) as task:
        log = task.run()
    return log
