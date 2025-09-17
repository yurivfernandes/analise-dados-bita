from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...tasks import LoadIncidentsOpened, LoadIncidentsUpdated


class LoadIncidentsView(APIView):
    """View que aciona as tasks de construção/atualização da base de incidents do ServiceNow"""

    def post(self, request, *args, **kwargs) -> Response:
        data_inicio = request.data.get("data_inicio")
        data_fim = request.data.get("data_fim")
        patch_requests_ssl()
        log = {}
        # task que popula pela data de opened_at (pode deletar+inserir)
        with LoadIncidentsOpened(
            start_date=data_inicio, end_date=data_fim
        ) as load:
            log["load_incidents_opened"] = load.run()

        # task que atualiza por sys_updated_on
        with LoadIncidentsUpdated(
            start_date=data_inicio, end_date=data_fim
        ) as load:
            log["load_incidents_updated"] = load.run()

        return Response(log)
