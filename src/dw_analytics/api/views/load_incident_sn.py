from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import LoadIncidentSN


class LoadIncidentSNView(APIView):
    """View que aciona a task de construção da base de [LoadIncidentsSN]"""

    def post(self, request, *args, **kwargs) -> Response:
        filtros = {}

        with LoadIncidentSN(**filtros) as load:
            log = load.run()
        return Response(log)

        # load_consolidacao_async.delay()
        # return Response(
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)
