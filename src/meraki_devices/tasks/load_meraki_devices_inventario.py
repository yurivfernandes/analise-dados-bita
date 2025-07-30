import os
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

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
            .fill_nan(None)
            .select(
                [
                    "name",
                    "serial",
                    "networkId",
                    "productType",
                    "model",
                    "address",
                    "lat",
                    "lng",
                    "notes",
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
                ]
            )
        )

    @property
    def _device_dataset(self) -> pl.DataFrame:
        """Retorna o DataSet de incidentes do Service Now."""
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
