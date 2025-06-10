from datetime import datetime

from rest_framework.request import Request
from rest_framework.response import Response

from .mixin_get_dataset import MixinGetDataset


class MixinViews(MixinGetDataset):
    def get(self, request: Request, *args, **kwargs) -> Response:
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
