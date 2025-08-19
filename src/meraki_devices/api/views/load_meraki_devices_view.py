import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import LoadMerakiDeviceInventario, LoadMerakiDevices
from ...utils import patch_requests_ssl

load_dotenv()


class LoadMerakiDevicesView(APIView):
    """View que aciona a task de construção da base de [Devices] do Meraki"""

    def post(self, request, *args, **kwargs) -> Response:
        patch_requests_ssl()
        log = {}
        # with LoadMerakiDevices(
        #     api_key=self.get_env_or_404(var_name="API_KEY_MERAKI")
        # ) as load:
        #     log["log_meraki_devices"] = load.run()
        with LoadMerakiDeviceInventario() as load:
            log["log_meraki_device_inventario"] = load.run()
        return Response(log)

        # load_consolidacao_async.delay()
        # return Response(
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)
        #     {"message": "A requisição foi recebida e a carga foi iniciada!"},
        #     status=status.HTTP_202_ACCEPTED)

    def get_env_or_404(self, var_name: str) -> str:
        value = os.getenv(var_name)
        if not value:
            raise ImproperlyConfigured(
                f"A variável de ambiente '{var_name}' não foi encontrada."
            )
        return value
