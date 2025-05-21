from datetime import datetime

import polars as pl
from django.db import models
from rest_framework.request import Request
from rest_framework.response import Response


class MixinViews:
    """MÉTODOS COMUNS PARA USO NAS VIEWS."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")

    def main(self) -> list:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")

    def valid_date(self, data_inicio: str, data_fim: str):
        """Valida se as datas passadas no request são válidas"""
        if not data_inicio or not data_fim:
            raise ValueError(
                "Ambas as datas, início e fim, devem ser fornecidas."
            )
        try:
            data_inicio_formatada = datetime.strptime(data_inicio, "%Y-%m-%d")
            data_fim_formatada = datetime.strptime(data_fim, "%Y-%m-%d")
        except ValueError:
            raise ValueError("As datas devem estar no formato 'aaaa-mm-dd'.")
        if data_inicio_formatada > data_fim_formatada:
            raise ValueError(
                "A data de início não pode ser posterior à data de fim."
            )
        return (data_inicio_formatada, data_fim_formatada)

    def get_dataset(
        self, query_set: models.QuerySet, schema: dict
    ) -> pl.DataFrame:
        """Retorna os dados do queryset em formato de dataframe. Recebe o queryset e o schema a ser aplicado no dataset"""
        return pl.DataFrame(
            data=list(query_set),
            schema=dict(**{k: v.get("type") for k, v in schema.items()}),
        ).rename({k: v["rename"] for k, v in schema.items()})

    def generate_schema_from_model(self, model: models):
        """Gera um schema de campos com todos os campos da model"""
        schema = {}
        for field in model._meta.get_fields():
            field_type = self.get_polars_type(field=field)
            schema[field.name] = {"rename": field.name, "type": field_type}
        return schema

    def get_polars_type(self, field: models.fields):
        """Mapeia tipos de campo Django para tipos de Polars."""
        if isinstance(field, models.AutoField) or isinstance(
            field, models.IntegerField
        ):
            return pl.Int64
        elif isinstance(field, models.CharField) or isinstance(
            field, models.TextField
        ):
            return pl.String
        elif isinstance(field, models.FloatField):
            return pl.Float64
        elif isinstance(field, models.DateField):
            return pl.Date
        elif isinstance(field, models.DateTimeField):
            return pl.Datetime
        else:
            return pl.String
