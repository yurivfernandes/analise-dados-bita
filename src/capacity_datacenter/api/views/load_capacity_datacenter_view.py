from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import (
    LoadNode,
    LoadInterface,
    LoadCustomPollerAssignment,
    LoadCapacityDatacenter,
    LoadCustompollerStatistics,
)


class LoadCapacityDatacenterView(APIView):
    """View que aciona o fluxo completo de carga (sem Celery)."""

    def post(self, request, *args, **kwargs) -> Response:
        """Executa em sequência: node -> interface -> custom poller assignment -> response_time -> custom poller statistics.

        Espera JSON body opcional com:
        - days_back: int (opcional) — repassado para os loaders que aceitam esse parâmetro
        """
        payload = request.data or {}
        days_back = payload.get("days_back")
        try:
            days_back = int(days_back) if days_back is not None else None
        except (TypeError, ValueError):
            days_back = None

        log = {}

        # 1) Nodes
        loader = LoadNode()
        log["load_node"] = loader.run()

        # 2) Interfaces
        loader = LoadInterface()
        log["load_interface"] = loader.run()

        # 3) Custom Poller Assignment
        loader = LoadCustomPollerAssignment()
        log["load_custom_poller_assignment"] = loader.run()

        # 4) Response Time (aceita days_back)
        loader = LoadCapacityDatacenter(days_back=days_back)
        log["load_response_time"] = loader.run()

        # 5) Custom Poller Statistics (aceita days_back)
        loader = LoadCustompollerStatistics(days_back=days_back)
        log["load_custom_poller_statistics"] = loader.run()

        return Response(log)
