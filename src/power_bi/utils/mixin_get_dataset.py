import polars as pl
from django.db import models

from .mixin_querys import MixinQuerys


class MixinGetDataset(MixinQuerys):
    def get_dataset(
        self, query_set: models.QuerySet, schema: dict
    ) -> pl.DataFrame:
        """Retorna os dados do queryset em formato de dataframe. Recebe o queryset e o schema a ser aplicado no dataset"""
        return pl.DataFrame(
            data=list(query_set),
            schema=dict(**{k: v.get("type") for k, v in schema.items()}),
        ).rename({k: v["rename"] for k, v in schema.items()})

    def generate_schema_from_model(self, model: models)->dict:
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
