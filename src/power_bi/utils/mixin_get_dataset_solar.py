from functools import cached_property

import polars as pl

from ..models import (
    SolarInterfaceOriginal,
    SolarNodeOriginal,
    SolarNomeClienteCorreto,
    SolarNomeOperadoraCorreto,
    SolarNomeTecnologiaCorreto,
)
from .mixin_get_dataset import MixinGetDataset


class MixinGetDatasetSolar(MixinGetDataset):
    @cached_property
    def _nome_tecnologia_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto da operadora."""
        schema = self.generate_schema_from_model(
            model=SolarNomeTecnologiaCorreto
        )
        return (
            self.get_dataset(
                query_set=self.get_nome_tecnologia_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "tecnologia"})
        )

    @cached_property
    def nome_operadora_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto da operadora."""
        schema = self.generate_schema_from_model(
            model=SolarNomeOperadoraCorreto
        )
        return (
            self.get_dataset(
                query_set=self.get_nome_operadora_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "operadora"})
        )

    @property
    def nome_cliente_correto(self) -> pl.DataFrame:
        """Retorna os registros com o nome correto do cliente."""
        schema = self.generate_schema_from_model(model=SolarNomeClienteCorreto)
        return (
            self.get_dataset(
                query_set=self.get_nome_cliente_correto_queryset().values(
                    *schema
                ),
                schema=schema,
            )
            .drop("id")
            .rename({"nome_solar": "nome_cliente"})
        )

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

    @property
    def solar_node_original(self) -> pl.DataFrame:
        """Retorna os registros as interfaces que foram importadas do solar."""
        print("...BUSCANDO OS DADOS DOS NODES...")
        schema = self.generate_schema_from_model(model=SolarNodeOriginal)
        return self.get_dataset(
            query_set=self.get_solar_node_original_queryset().values(*schema),
            schema=schema,
        )
