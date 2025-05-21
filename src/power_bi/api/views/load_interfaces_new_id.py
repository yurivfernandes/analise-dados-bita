import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import LoadInterfaceNewID


class LoadInterfaceNewIDVGR(APIView):
    """View que aciona a task de construção da base de [Consolidacao]"""

    def post(self, request, *args, **kwargs) -> Response:
        filtros = {
            "company_remedy_list": request.data.get("company_remedy", []),
            "nome_do_cliente_list": request.data.get("nome_do_cliente", []),
        }

        with LoadInterfaceNewID(**filtros) as load:
            log = load.run()
        return Response(log)

        # load_consolidacao_async.delay()
        # return Response(
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)
