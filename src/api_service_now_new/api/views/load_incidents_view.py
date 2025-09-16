import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks.load_incidents_opened import LoadIncidentsOpened
from ...tasks.load_incidents_updated import LoadIncidentsUpdated


class LoadIncidentsView(APIView):
    """View que aciona as tasks de construção/atualização da base de incidents do ServiceNow"""

    def post(self, request, *args, **kwargs) -> Response:
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        log = {}
        # task que popula pela data de opened_at (pode deletar+inserir)
        with LoadIncidentsOpened(
            start_date=start_date, end_date=end_date
        ) as load:
            log["load_incidents_opened"] = load.run()

        # task que atualiza por sys_updated_on
        with LoadIncidentsUpdated(
            start_date=start_date, end_date=end_date
        ) as load:
            log["load_incidents_updated"] = load.run()

        return Response(log)
