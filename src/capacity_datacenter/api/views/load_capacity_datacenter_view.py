from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import (
    LoadCustomPollerAssignment,
    LoadCustompollerStatistics,
    LoadInterface,
    LoadInterfaceTraffic,
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

        # # 2) Interfaces
        # loader = LoadInterface()
        # log["load_interface"] = loader.run()

        # # 3) Custom Poller Assignment
        # loader = LoadCustomPollerAssignment()
        # log["load_custom_poller_assignment"] = loader.run()

        # # 4) Response Time (recebe start_date/end_date)

        # statistics_logs = []
        # if start_date and end_date:
        #     current_date = start_date
        #     print(f"Data atual: {current_date}")
        #     while current_date <= end_date:
        #         loader = LoadResponseTime(
        #             start_date=current_date, end_date=current_date
        #         )
        #         result = loader.run()
        #         statistics_logs.append({str(current_date): result})
        #         current_date += timedelta(days=1)
        #         print(f"Data atual: {current_date}")
        # else:
        #     loader = LoadResponseTime(start_date=start_date, end_date=end_date)
        #     statistics_logs.append({"single_run": loader.run()})

        # log["load_response_time"] = statistics_logs

        # 5) Custom Poller Statistics (executa uma vez por dia)
        # statistics_logs = []
        # if start_date and end_date:
        #     current_date = start_date
        #     print(f"Data atual: {current_date}")
        #     while current_date <= end_date:
        #         loader = LoadCustompollerStatistics(
        #             start_date=current_date, end_date=current_date
        #         )
        #         result = loader.run()
        #         statistics_logs.append({str(current_date): result})
        #         current_date += timedelta(days=1)
        #         print(f"Data atual: {current_date}")
        # else:
        #     loader = LoadCustompollerStatistics(
        #         start_date=start_date, end_date=end_date
        #     )
        #     statistics_logs.append({"single_run": loader.run()})

        # log["load_custom_poller_statistics"] = statistics_logs

        # # 6) Interface Traffic (executa uma vez por dia)
        # statistics_logs = []
        # if start_date and end_date:
        #     current_date = start_date
        #     print(f"Data atual: {current_date}")
        #     while current_date <= end_date:
        #         loader = LoadInterfaceTraffic(
        #             start_date=current_date, end_date=current_date
        #         )
        #         result = loader.run()
        #         statistics_logs.append({str(current_date): result})
        #         current_date += timedelta(days=1)
        #         print(f"Data atual: {current_date}")
        # else:
        #     loader = LoadInterfaceTraffic(
        #         start_date=start_date, end_date=end_date
        #     )
        #     statistics_logs.append({"single_run": loader.run()})

        # log["load_custom_poller_statistics"] = statistics_logs

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
