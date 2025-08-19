import os

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from ...tasks import LoadContractSLA
from ...utils import patch_requests_ssl

load_dotenv()


class LoadContractSLAView(APIView):
    """View que aciona a task de construção da base de [Devices] do Meraki"""

    def post(self, request, *args, **kwargs) -> Response:
        log = {}
        patch_requests_ssl()
        params = {
            "service_now_base_url": self.get_env_or_404(
                var_name="SERVICE_NOW_BASE_URL"
            ),
            "service_now_username": self.get_env_or_404(
                var_name="SERVICE_NOW_USERNAME"
            ),
            "service_now_user_password": self.get_env_or_404(
                var_name="SERVICE_NOW_USER_PASSWORD"
            ),
        }
        with LoadContractSLA(params=params) as load:
            log["log"] = load.run()

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
