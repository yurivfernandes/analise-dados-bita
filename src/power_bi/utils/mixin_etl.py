import polars as pl
from django.db import connection


class MixinETL:
    """Classe que define como será o etl dos datasets do Solar."""

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
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")
