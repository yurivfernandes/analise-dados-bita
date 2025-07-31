import os
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline
from power_bi.models.solar_nome_operadora_correto import (
    SolarNomeOperadoraCorreto,
)

from ..models import Device, DeviceInventario
from ..utils import MixinQuerys


class LoadMerakiDeviceInventario(MixinGetDataset, MixinQuerys, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()
        self.load(dataset=self.dataset, model=DeviceInventario, filtro={})
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = (
            self._device_dataset.pipe(self._assign_status_migrado)
            .pipe(self._expand_notes)
            .with_columns(
                pl.col("name")
                .str.strip_chars()
                .str.replace_all(r"\s+", "")
                .alias("name")
            )
            .pipe(self._add_tecnologia_columns)
            .pipe(self._add_operadora_columns)
            .pipe(self._add_lp_columns)
            .pipe(self._add_velocidade_columns)
            .pipe(self._select_final_columns)
            .fill_nan(None)
        )

    def _add_velocidade_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Adiciona as colunas velocidade_1, velocidade_2 e velocidade_3 ao DataFrame, extraindo o valor em Mbps das notas."""
        return df.with_columns(
            [
                pl.col("note_1")
                .map_elements(self._get_velocidade, return_dtype=pl.Int64)
                .alias("velocidade_1"),
                pl.col("note_2")
                .map_elements(self._get_velocidade, return_dtype=pl.Int64)
                .alias("velocidade_2"),
                pl.col("note_3")
                .map_elements(self._get_velocidade, return_dtype=pl.Int64)
                .alias("velocidade_3"),
            ]
        )

    def _get_velocidade(self, note):
        """Extrai o valor numérico da velocidade em Mbps da string da nota. Retorna int ou None."""
        import re

        if not isinstance(note, str):
            return None
        match = re.search(r"(\d+)\s*mbps", note, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    @property
    def _device_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de dispositivos Meraki."""
        schema = self.generate_schema_from_model(model=Device)
        query_set = self.get_device_queryset().values(*schema.keys())

        return self.get_dataset(
            query_set=query_set,
            schema=schema,
        )

    def _assign_status_migrado(self, devices: pl.DataFrame) -> pl.DataFrame:
        """Define se os devices estão migrados ou não."""
        return devices.with_columns(
            [
                pl.col("name")
                .str.split("_")
                .map_elements(
                    lambda partes: (
                        f"MCD_{partes[1]}_{partes[2]}"
                        if len(partes) > 2 and "KSK" in partes[2]
                        else f"MCD_{partes[1]}"
                        if len(partes) > 1
                        else "MCD_UNKNOWN"
                    ),
                    return_dtype=pl.String,
                )
                .alias("sigla")
            ]
        ).with_columns(
            pl.when(pl.col("sigla").str.contains("KSK"))
            .then(
                pl.col("sigla").map_elements(
                    lambda k: self._sigla_quiosque.get(k, False),
                    return_dtype=pl.Boolean,
                )
            )
            .otherwise(
                pl.col("sigla").map_elements(
                    lambda k: self._sigla_restaurante.get(k, False),
                    return_dtype=pl.Boolean,
                )
            )
            .alias("status_migrado")
        )

    @cached_property
    def _migrados(self) -> pl.DataFrame:
        """Retorna o dataset com a planilha de migrados."""
        migrados_path = os.path.join(
            os.path.dirname(__file__), "Migrados.xlsx"
        )

        if not os.path.exists(migrados_path):
            print(
                f"Arquivo Migrados.xlsx não encontrado na raiz do projeto: {migrados_path}"
            )
            return pl.DataFrame()

        try:
            return (
                pl.read_excel(migrados_path)
                .rename(
                    {
                        col: col.strip().lower().replace(" ", "_")
                        for col in pl.read_excel(migrados_path).columns
                    }
                )
                .select("sigla", "sigla_revista", "tipo_2")
            )
        except Exception as e:
            print(f"Erro ao ler o arquivo Migrados.xlsx: {e}")
            return pl.DataFrame()

    @property
    def _sigla_restaurante(self) -> dict:
        """Retorna um dict com siglas dos restaurantes e valor True"""
        return {
            f"MCD_{sigla.strip().upper()}": True
            for sigla in self._migrados.filter(
                pl.col("tipo_2").str.to_uppercase() == "RESTAURANTE"
            )
            .select(pl.col("sigla"))
            .drop_nulls()
            .to_series()
            .to_list()
        }

    @property
    def _sigla_quiosque(self) -> dict:
        """Retorna um dict com as siglas de quiosques e valor True"""
        return {
            f"MCD_{sigla}": True
            for sigla in (
                self._migrados.filter(
                    pl.col("tipo_2").str.to_uppercase() == "QUIOSQUE"
                )
                .select(
                    pl.col("sigla_revista")
                    .str.replace("MCD_", "")
                    .str.strip_chars()
                    .str.to_uppercase()
                )
                .drop_nulls()
                .to_series()
                .to_list()
            )
        }

    def _split_notes(self, notes: str) -> dict:
        """Divide as notas em partes e retorna um dicionário com as partes numeradas."""
        if isinstance(notes, str):
            parts = notes.split("\n\n")
            return {
                f"note_{i + 1}": part.strip() for i, part in enumerate(parts)
            }
        return {}

    def _expand_notes(self, df: pl.DataFrame) -> pl.DataFrame:
        """Expande os notes para outras colunas"""
        return df.with_columns(
            pl.DataFrame(
                [
                    self._split_notes(n)
                    for n in df.select("notes").to_series().to_list()
                ]
            )
        )

    def _add_tecnologia_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Adiciona as colunas tecnologia_1, tecnologia_2 e tecnologia_3 ao DataFrame, baseando-se nas notas. Considera 'BL' como 'BANDA LARGA' e faz upper case antes de testar."""
        return df.with_columns(
            [
                pl.when(
                    pl.col("note_1")
                    .str.to_uppercase()
                    .str.contains("IP DEDICADO")
                )
                .then(pl.lit("IP DEDICADO"))
                .when(
                    pl.col("note_1")
                    .str.to_uppercase()
                    .str.contains("BANDA LARGA|BL")
                )
                .then(pl.lit("BANDA LARGA"))
                .otherwise(pl.lit(None))
                .alias("tecnologia_1"),
                pl.when(
                    pl.col("note_2")
                    .str.to_uppercase()
                    .str.contains("IP DEDICADO")
                )
                .then(pl.lit("IP DEDICADO"))
                .when(
                    pl.col("note_2")
                    .str.to_uppercase()
                    .str.contains("BANDA LARGA|BL")
                )
                .then(pl.lit("BANDA LARGA"))
                .otherwise(pl.lit(None))
                .alias("tecnologia_2"),
                pl.when(
                    pl.col("note_3")
                    .str.to_uppercase()
                    .str.contains("IP DEDICADO")
                )
                .then(pl.lit("IP DEDICADO"))
                .when(
                    pl.col("note_3")
                    .str.to_uppercase()
                    .str.contains("BANDA LARGA|BL")
                )
                .then(pl.lit("BANDA LARGA"))
                .otherwise(pl.lit(None))
                .alias("tecnologia_3"),
            ]
        )

    def _add_operadora_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Adiciona as colunas nome_operadora_1, nome_operadora_2 e nome_operadora_3 ao DataFrame, pesquisando as operadoras nas notas."""
        return df.with_columns(
            [
                pl.col("note_1")
                .map_elements(self._find_operadora, return_dtype=pl.String)
                .alias("nome_operadora_1"),
                pl.col("note_2")
                .map_elements(self._find_operadora, return_dtype=pl.String)
                .alias("nome_operadora_2"),
                pl.col("note_3")
                .map_elements(self._find_operadora, return_dtype=pl.String)
                .alias("nome_operadora_3"),
            ]
        )

    def _find_operadora(self, note):
        """Busca o nome da operadora na string da nota, retornando o nome correto (palavra inteira) ou None."""
        import re

        if not isinstance(note, str):
            return None
        note_lower = note.lower()
        for op in self._lista_operadoras:
            if not op:
                continue
            # Regex para encontrar a operadora como palavra inteira, ignorando case
            pattern = r"(?<!\w)" + re.escape(op.lower()) + r"(?!\w)"
            if re.search(pattern, note_lower):
                return op
        return None

    @cached_property
    def _lista_operadoras(self) -> list:
        """Retorna uma lista de nome_correto das operadoras."""
        return list(
            SolarNomeOperadoraCorreto.objects.values_list(
                "nome_correto", flat=True
            )
        )

    def _add_lp_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Adiciona as colunas LP_1, LP_2 e LP_3 ao DataFrame, extraindo o código LP das notas."""
        return df.with_columns(
            [
                pl.col("note_1")
                .map_elements(self._get_lp, return_dtype=pl.String)
                .alias("LP_1"),
                pl.col("note_2")
                .map_elements(self._get_lp, return_dtype=pl.String)
                .alias("LP_2"),
                pl.col("note_3")
                .map_elements(self._get_lp, return_dtype=pl.String)
                .alias("LP_3"),
            ]
        )

    def _get_lp(self, note):
        """Extrai o código LP da string da nota, removendo traço final se houver, ou retorna None."""
        import re

        if not isinstance(note, str):
            return None
        match = re.search(r"LP:\s*([^\s]+)", note)
        if match:
            codigo = match.group(1)
            if codigo.endswith("-"):
                codigo = codigo[:-1]
            return codigo
        return None

    def _select_final_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Seleciona as colunas finais do DataFrame para o inventário de dispositivos Meraki."""
        return df.select(
            [
                "name",
                "serial",
                "networkId",
                "productType",
                "model",
                "address",
                "lat",
                "lng",
                "wan1Ip",
                "wan2Ip",
                "firmware",
                "organization_id",
                "lanIp",
                "sigla",
                "status_migrado",
                "note_1",
                "note_2",
                "note_3",
                "tecnologia_1",
                "tecnologia_2",
                "tecnologia_3",
                "nome_operadora_1",
                "nome_operadora_2",
                "nome_operadora_3",
                "LP_1",
                "LP_2",
                "LP_3",
            ]
        )


@shared_task(
    name="meraki.load_meraki_devices_inventario",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_meraki_devices_inventario_async(self) -> Dict:
    sync_task = LoadMerakiDeviceInventario()
    return sync_task.run()
