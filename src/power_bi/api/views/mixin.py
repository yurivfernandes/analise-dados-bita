from datetime import datetime

import polars as pl
from django.db import models
from rest_framework.request import Request
from rest_framework.response import Response


class Mixin:
    def get(self, request: Request, *args, **kwargs) -> Response:
        self.data_range = self._valid_date(
            data_inicio=request.GET.get("data_inicio"),
            data_fim=request.GET.get("data_fim"),
        )
        self._set_date_maps()
        return Response(self.main())

    def _valid_date(self, data_inicio: str, data_fim: str):
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

    def main(self) -> list:
        """Implementar o método main retornando um DataFrame"""
        raise NotImplementedError("Subclass must implement this method")

    def _get_dataset(
        self, query_set: models.QuerySet, schema: dict
    ) -> pl.DataFrame:
        """Retorna os dados do queryset em formato de dataframe"""
        return pl.DataFrame(
            data=list(query_set),
            schema=dict(**{k: v.get("type") for k, v in schema.items()}),
        ).rename({k: v["rename"] for k, v in schema.items()})
