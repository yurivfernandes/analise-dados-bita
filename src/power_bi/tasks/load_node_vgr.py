import re
from functools import cached_property
from itertools import islice

import polars as pl

# from celery import shared_task
from django.db import connection, transaction
from django.db.models import QuerySet

from app.utils.pipeline import Pipeline
from correios.models import TblCepNLogradouro

from ..models import (
    SolarNode,
    SolarNodeOriginal,
    SolarNomeClienteCorreto,
    SolarNomeOperadoraCorreto,
    SolarNomeTecnologiaCorreto,
)
from ..utils.mixin import MixinViews


class LoadNodeVGR(MixinViews, Pipeline):
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

    def _get_solar_node_original_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto do cliente"""
        return SolarNodeOriginal.objects.using("power_bi").filter(
            **self._filtro
        )

    def _get_nome_operadora_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto da operadora"""
        return SolarNomeOperadoraCorreto.objects.using("power_bi")

    def _get_nome_tecnologia_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto da operadora"""
        return SolarNomeTecnologiaCorreto.objects.using("power_bi")

    def _get_nome_cliente_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto do cliente"""
        return SolarNomeClienteCorreto.objects.using("power_bi")

    def _get_uf_and_municipio_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto do cliente"""
        return TblCepNLogradouro.objects.using("correios")

    def run(self) -> dict:
        self.extract_transform_dataset()
        print("DATASET PRONTO PARA SER INSERIDO NO BANCO!")
        self.load()
        print("DADOS SALVOS NO BANCO, FINALIZANDO...")
        return self.log

    def extract_transform_dataset(self) -> None:
        """Extrai e transforma o dataset principal incluindo log de IDs antigos."""
        self.dataset = (
            self._solar_node_original.pipe(self._limpar_texto)
            .pipe(self._corrigir_operadoras)
            .pipe(self._corrigir_tecnologias)
            .pipe(self._corrigir_nome_cliente)
            .pipe(self._get_uf_and_municipio)
            .pipe(self._corrigir_municipio_uf)
            .pipe(self._get_novo_id_vgr)
            .select(
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
                    "ip_node",
                    "historico_ids",
                ]
            )
        )

    @property
    def _solar_node_original(self) -> pl.DataFrame:
        """Retorna os registros as interfaces que foram importadas do solar."""
        print("BUSCANDO OS DADOS INICIAIS...")
        schema = self.generate_schema_from_model(model=SolarNodeOriginal)
        return self.get_dataset(
            query_set=self._get_solar_node_original_queryset().values(*schema),
            schema=schema,
        )

    def _limpar_texto(self, df: pl.DataFrame) -> pl.DataFrame:
        """Limpa o texto das colunas que tem texto."""
        print("LIMPANDO TEXTO...")
        return df.select(
            [
                pl.col(col)
                .cast(pl.Utf8)
                .replace({"None": None, "none": None, "NONE": None, "": None})
                .str.strip_chars()
                .str.replace(r"\s+", " ")
                for col in df.columns
            ]
        ).with_columns(pl.col("cep").str.replace("-", ""))

    def _corrigir_operadoras(self, df: pl.DataFrame) -> pl.DataFrame:
        """Corrige o nome das operadores conforme a tabela [SolarNomeOperadoraCorreto] e tenta buscar o nome da operadora em outras colunas."""
        print("CORRIGINDO OPERADORAS...")
        return (
            df.join(self._nome_operadora_correto, how="left", on="operadora")
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

    @cached_property
    def _nome_operadora_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto da operadora."""
        schema = self.generate_schema_from_model(
            model=SolarNomeOperadoraCorreto
        )
        return (
            self.get_dataset(
                query_set=self._get_nome_operadora_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "operadora"})
        )

    def encontrar_operadora(self, nome_interface: str) -> str | None:
        """Verifica se o nome da operadora aparece parcialmente dentro de interface name."""
        if nome_interface in (
            "",
            None,
            "Null",
            "null",
            " ",
            "none",
            "None",
            "-",
            "N/A",
            "#N/A",
        ):
            return None
        operadoras_corretas = (
            self._nome_operadora_correto["nome_correto"].unique().to_list()
        )
        for operadora in operadoras_corretas:
            if re.search(
                rf"\b{re.escape(operadora)}\b", nome_interface, re.IGNORECASE
            ):
                if operadora == "CLARO":
                    return operadora
        return None

    @cached_property
    def _nome_tecnologia_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto da operadora."""
        schema = self.generate_schema_from_model(
            model=SolarNomeTecnologiaCorreto
        )
        return (
            self.get_dataset(
                query_set=self._get_nome_tecnologia_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "tecnologia"})
        )

    def _corrigir_tecnologias(self, df: pl.DataFrame) -> pl.DataFrame:
        """CORRIGE OS NOMES DAS TECNOLOGIAS"""
        print("CORRIGINDO TECNOLOGIAS...")
        return (
            df.join(self._nome_tecnologia_correto, how="left", on="tecnologia")
            .with_columns(
                pl.when(
                    pl.col("nome_correto").is_in(
                        [
                            None,
                            "null",
                            "NULL",
                            "Null",
                            "NONE",
                            "None",
                            "none",
                            "N/A",
                            "#N/A",
                            "n/a0",
                            "2",
                            "-",
                            " ",
                        ]
                    )
                )
                .then(pl.col("tecnologia"))
                .otherwise(pl.col("nome_correto"))
                .alias("tecnologia")
            )
            .drop("nome_correto")
        )

    def _corrigir_nome_cliente(self, df: pl.DataFrame) -> pl.DataFrame:
        """CORRIGE NOS NOMES DAS COMPANYS"""
        print("CORRIGINDO NOME DOS CLIENTES...")
        return (
            df.with_columns(
                pl.when(
                    pl.col("razao_social").is_in(
                        [None, "null", "NULL", "Null", "NONE", "None", "none"]
                    )
                )
                .then(pl.col("razao_social"))
                .otherwise(pl.col("nome_cliente"))
                .alias("nome_cliente"),
            )
            .join(self._nome_cliente_correto, how="left", on="nome_cliente")
            .with_columns(
                pl.when(pl.col("nome_correto").is_null())
                .then(pl.col("nome_cliente"))
                .otherwise(pl.col("nome_correto"))
                .alias("nome_cliente")
            )
            .drop("nome_correto")
        )

    @property
    def _nome_cliente_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto do cliente."""
        schema = self.generate_schema_from_model(model=SolarNomeClienteCorreto)
        return (
            self.get_dataset(
                query_set=self._get_nome_cliente_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "nome_cliente"})
        )

    def _get_uf_and_municipio(self, df: pl.DataFrame) -> pl.DataFrame:
        """Atribui a cidade e a uf com base na lista de CEP's do dataset"""
        print("ATRIBUINDO OS DADOS DE UF E MUNICÍPIO DA BASE DOS CORREIOS...")
        cep_list = (
            df.with_columns(pl.col("cep").cast(pl.String))
            .select("cep")
            .filter(~pl.col("cep").is_in(["NULL"]))
            .drop_nulls()
            .unique()
            .to_series()
            .to_list()
        )
        return df.join(
            self._get_correios_uf_and_municipio(cep_list=cep_list),
            on="cep",
            how="left",
        )

    def _get_correios_uf_and_municipio(self, cep_list: list) -> pl.DataFrame:
        """Retorna os dados de UF e Município com base nos CEP's que ja existem no dataset."""
        schema = {
            "cep": {"rename": "cep", "dtype": pl.String},
            "estado": {"rename": "uf", "dtype": pl.String},
            "cidade_id__cidade_sem_acento": {
                "rename": "municipio",
                "dtype": pl.String,
            },
        }
        resultados = []

        for chunk in self._chunked_iterable(cep_list, 2000):
            query_set = (
                self._get_uf_and_municipio_queryset()
                .filter(cep__in=chunk)
                .values(*schema.keys())
            )
            resultados.append(
                self.get_dataset(query_set=query_set, schema=schema)
            )

        return pl.concat(resultados)

    def _chunked_iterable(self, iterable, size):
        """Divide uma lista em partes menores."""
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    def _corrigir_municipio_uf(self, df: pl.DataFrame) -> pl.DataFrame:
        """CORRIGE OS NOMES DOS MUNICÍPIOS DE ACORDO COM O BANCO DOS CORREIOS"""
        print("CORRIGINDO UF E MUNICIPIO...")
        return df.with_columns(
            pl.col("municipio").str.to_uppercase().alias("municipio"),
            pl.col("uf").str.to_uppercase().alias("uf"),
        ).with_columns(
            pl.when(
                pl.col("uf").is_in(
                    [None, "null", "NULL", "Null", "NONE", "None", "none"]
                )
            )
            .then(None)
            .otherwise(pl.col("uf"))
            .alias("uf"),
            pl.when(
                pl.col("municipio").is_in(
                    [None, "null", "NULL", "Null", "NONE", "None", "none"]
                )
            )
            .then(None)
            .otherwise(pl.col("municipio"))
            .alias("municipio"),
        )

    def _get_novo_id_vgr(self, df: pl.DataFrame) -> pl.DataFrame:
        """Busca os novos ID's VGR"""
        print("BUSCANDO NOVO ID VGR....")
        new_id_dataframe = (
            df.filter(
                ~pl.col("status_vantive").is_in(
                    ["RFS Faturável", "RFS Técnico"]
                )
                | pl.col("status_vantive").is_null()
            )
            .with_columns(
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
                    lambda row: self._get_final_id_vgr(
                        row["id_vgr"], row["status_vantive"]
                    ),
                    return_dtype=pl.Struct,
                )
                .alias("novo_valores")
            )
            .with_columns(
                pl.col("novo_valores")
                .struct.field("id_vgr")
                .cast(str)
                .alias("id_vgr"),
                pl.col("novo_valores")
                .struct.field("status_vantive")
                .cast(str)
                .alias("status_vantive"),
                pl.col("novo_valores")
                .struct.field("historico_ids")
                .alias("historico_ids"),
            )
            .drop("novo_valores")
        )

        faturavel_and_tecnico_dataset = df.filter(
            pl.col("status_vantive").is_in(["RFS Faturável", "RFS Técnico"])
            | ~pl.col("status_vantive").is_null()
        ).with_columns(
            pl.lit([]).cast(pl.List(pl.Utf8)).alias("historico_ids")
        )

        return pl.concat([faturavel_and_tecnico_dataset, new_id_dataframe])

    def _get_final_id_vgr(self, id_vgr: str, status_vantive: str) -> dict:
        """Busca o ID final iterativamente e mantém um log de IDs."""
        historico_ids = []
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
            result = self._query_sae(id_vgr)
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

    def _query_sae(self, id_vgr: str) -> dict:
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
        print("LIMPANDO A BASE NO BANCO DE DADOS...")
        n_deleted, __ = (
            SolarNode.objects.using("power_bi").filter(**self._filtro).delete()
        )
        self.log["n_deleted"] = n_deleted

    def _save(self):
        print("SALVANDO OS DADOS NO BANCO DE DADOS...")
        if self.dataset.is_empty():
            return

        objs = [SolarNode(**vals) for vals in self.dataset.to_dicts()]
        bulk = SolarNode.objects.using("power_bi").bulk_create(
            objs=objs, batch_size=1000
        )
        self.log["n_inserted"] = len(bulk)


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
