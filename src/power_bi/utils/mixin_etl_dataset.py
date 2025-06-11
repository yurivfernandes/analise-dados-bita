import re
from itertools import islice

import polars as pl
from django.db import connection


class MixinETLDataset:
    """Classe que define como será o etl dos datasets do Solar."""

    def transform_dataset(self, dataset: pl.DataFrame) -> pl.DataFrame:
        """Extrai e transforma o dataset principal incluindo log de IDs antigos."""
        return (
            dataset.pipe(self.limpar_texto)
            .pipe(self.corrigir_operadoras)
            .pipe(self.corrigir_tecnologias)
            .pipe(self.corrigir_nome_cliente)
            .pipe(self.get_uf_and_municipio)
            .pipe(self.corrigir_uf_and_municipio)
            .pipe(self.get_novo_id_vgr)
            .pipe(self.selecionar_colunas)
        )

    def limpar_texto(self, df: pl.DataFrame) -> pl.DataFrame:
        """Limpa o texto das colunas que tem texto."""
        print("...LIMPANDO OS TEXTO DE TODAS AS COLUNAS...")
        return df.select(
            [
                pl.col(col)
                .cast(pl.Utf8)
                .replace(
                    {
                        "None": None,
                        "none": None,
                        "NONE": None,
                        "": None,
                        "N/A": None,
                        "n/a": None,
                        "N/a": None,
                        "null": None,
                        "NULL": None,
                        "[null]": None,
                        "[NULL]": None,
                    }
                )
                .str.strip_chars()
                .str.replace(r"\s+", " ")
                for col in df.columns
            ]
        ).with_columns(pl.col("cep").str.replace("-", ""))

    def corrigir_operadoras(self, df: pl.DataFrame) -> pl.DataFrame:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")

    def encontrar_operadora(self, nome_interface: str) -> str | None:
        """Busca o nome de operadora em outras colunas e corrige o nome com o de x para"""
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
            self.nome_operadora_correto["nome_correto"].unique().to_list()
        )
        for operadora in operadoras_corretas:
            if re.search(
                rf"\b{re.escape(operadora)}\b", nome_interface, re.IGNORECASE
            ):
                return operadora
        return None

    def corrigir_tecnologias(self, df: pl.DataFrame) -> pl.DataFrame:
        """Busca o nome da tecnologia no de x para e corrige."""
        print("...BUSCANDO E CORRIGINDO OS NOMES DE TECNOLOGIAS...")
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

    def corrigir_nome_cliente(self, df: pl.DataFrame) -> pl.DataFrame:
        """CORRIGE NOS NOMES DAS COMPANYS"""
        print("...CORRIGINDO NOME DOS CLIENTES...")
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
            .join(self.nome_cliente_correto, how="left", on="nome_cliente")
            .with_columns(
                pl.when(pl.col("nome_correto").is_null())
                .then(pl.col("nome_cliente"))
                .otherwise(pl.col("nome_correto"))
                .alias("nome_cliente")
            )
            .drop("nome_correto")
        )

    def get_uf_and_municipio(self, df: pl.DataFrame) -> pl.DataFrame:
        """Atribui a cidade e a uf com base na lista de CEP's do dataset"""
        print(
            "...ATRIBUINDO OS DADOS DE UF E MUNICÍPIO DA BASE DOS CORREIOS COM BASE NO CEP DO ID NO SAE..."
        )
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
            self.get_correios_uf_and_municipio(cep_list=cep_list),
            on="cep",
            how="left",
        )

    def get_correios_uf_and_municipio(self, cep_list: list) -> pl.DataFrame:
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

        for chunk in self.chunked_iterable(cep_list, 2000):
            query_set = (
                self.get_uf_and_municipio_queryset()
                .filter(cep__in=chunk)
                .values(*schema.keys())
            )
            resultados.append(
                self.get_dataset(query_set=query_set, schema=schema)
            )

        return pl.concat(resultados)

    def chunked_iterable(self, iterable, size):
        """Divide uma lista em partes menores."""
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    def corrigir_uf_and_municipio(self, df: pl.DataFrame) -> pl.DataFrame:
        """Corrige a UF e Município de acordo com a base dos correios"""
        print(
            "...CORRIGINDO UF E MUNICIPIO DE ACORDO COM A BASE DOS CORREIOS..."
        )
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

    def get_novo_id_vgr(self, df: pl.DataFrame) -> pl.DataFrame:
        """Com base nos ID's VGR de cada interface, busca o status correto e o novo ID caso exista."""
        print(
            "...CORRIGINDO O STATUS VANTIVE E BUSCANDO NOVOS IDS VGR QUANDO EXISTEM...."
        )
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
                    lambda row: self.get_final_id_vgr(
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

    def get_final_id_vgr(self, id_vgr: str, status_vantive: str) -> dict:
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

    def selecionar_colunas(self, df: pl.DataFrame) -> pl.DataFrame:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")
