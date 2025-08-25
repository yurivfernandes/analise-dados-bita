from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import (
    LoadCustomPollerAssignment,
    LoadCustompollerStatistics,
    LoadInterface,
    LoadNode,
    LoadResponseTime,
)


class LoadCapacityDatacenterView(APIView):
    """View que aciona o fluxo completo de carga (sem Celery)."""

    def post(self, request, *args, **kwargs) -> Response:
        payload = request.data or {}

        start_date = self._parse_date(
            payload, "data_inicio"
        ) or self._parse_date(payload, "date_inicio")
        end_date = self._parse_date(payload, "data_fim") or self._parse_date(
            payload, "date_fim"
        )

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

        # 4) Response Time (recebe start_date/end_date)
        loader = LoadResponseTime(start_date=start_date, end_date=end_date)
        log["load_response_time"] = loader.run()

        # 5) Custom Poller Statistics (recebe start_date/end_date)
        loader = LoadCustompollerStatistics(
            start_date=start_date, end_date=end_date
        )
        log["load_custom_poller_statistics"] = loader.run()

        return Response(log)

    def _parse_date(self, payload: dict, key: str):
        """Tenta parsear `YYYY-MM-DD` ou retorna None.

        Observação: esta função está definida fora de `post` por preferência do autor
        (usa-se `payload` explicitamente como primeiro argumento).
        """
        val = payload.get(key) if payload else None
        if not val:
            return None
        try:
            return datetime.strptime(val, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None
