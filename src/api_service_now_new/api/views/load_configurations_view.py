import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...tasks import LoadContractSla, LoadGroups, LoadSysCompany, LoadSysUser

logger = logging.getLogger(__name__)


class LoadConfigurationsView(APIView):
    """View que aciona tasks de configurações do ServiceNow (contract_sla, groups, companies, users).

    Executa em thread de background, sem Celery, para evitar broken pipe na resposta HTTP.
    """

    def post(self, request, *args, **kwargs) -> Response:
        # as tasks de configuração não exigem start/end mas mantemos compatibilidade
        data_inicio = request.data.get("data_inicio")
        data_fim = request.data.get("data_fim")
        # se não informado, usar dia anterior
        if not data_inicio or not data_fim:
            ontem = (
                datetime.datetime.now() - datetime.timedelta(days=1)
            ).date()
            data_inicio = data_inicio or ontem.strftime("%Y-%m-%d")
            data_fim = data_fim or ontem.strftime("%Y-%m-%d")

        patch_requests_ssl()
        thread = threading.Thread(
            target=self._run_pipelines_in_background,
            args=(data_inicio, data_fim),
            daemon=True,
        )
        thread.start()

        return Response(
            {
                "status": "accepted",
                "message": "Processing started in background",
            }
        )

    def _run_pipelines_in_background(self, start_date, end_date):
        try:
            # contract_sla
            with LoadContractSla() as load:
                r1 = load.run()
                logger.info("load_contract_sla finished: %s", r1)

            # groups
            with LoadGroups() as load:
                r2 = load.run()
                logger.info("load_groups finished: %s", r2)

            # companies
            with LoadSysCompany() as load:
                r3 = load.run()
                logger.info("load_sys_company finished: %s", r3)

            # users
            with LoadSysUser() as load:
                r4 = load.run()
                logger.info("load_sys_user finished: %s", r4)

        except Exception:
            logger.exception("Erro ao executar as pipelines de configurations")
