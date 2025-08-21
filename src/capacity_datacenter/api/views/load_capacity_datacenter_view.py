import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import LoadCapacityDatacenter, load_capacity_datacenter_async


class LoadCapacityDatacenterView(APIView):
    """View que aciona a task de construção da base de [Devices] do Meraki"""

    def post(self, request, *args, **kwargs) -> Response:
        log = {}
        with LoadCapacityDatacenter() as load:
            log["log_meraki_device_inventario"] = load.run()
        return Response(log)

        # load_capacity_datacenter_async.delay()
        # return Response(
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)
