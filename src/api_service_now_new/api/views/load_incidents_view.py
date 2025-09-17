import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...tasks import LoadIncidentsOpened, LoadIncidentsUpdated

logger = logging.getLogger(__name__)


class LoadIncidentsView(APIView):
    """View que aciona as tasks de construção/atualização da base de incidents do ServiceNow

    Agora executa o processamento pesado em uma thread de background para evitar
    que a conexão HTTP que chamou a view seja fechada (broken pipe) antes da conclusão.
    Não usa Celery — executa sincronamente em background dentro do processo do Django.
    """

    def post(self, request, *args, **kwargs) -> Response:
        data_inicio = request.data.get("data_inicio")
        data_fim = request.data.get("data_fim")
        patch_requests_ssl()
        thread = threading.Thread(
            target=self._run_pipelines_in_background,
            args=(data_inicio, data_fim),
            daemon=True,
        )
        thread.start()

        # retornar imediatamente informando que o processamento foi aceito
        return Response(
            {
                "status": "accepted",
                "message": "Processing started in background",
            }
        )

    def _run_pipelines_in_background(self, start_date, end_date):
        """Método que executa as pipelines em background (chamado pela thread)."""
        try:
            # task que popula pela data de opened_at (pode deletar+inserir)
            with LoadIncidentsOpened(
                start_date=start_date, end_date=end_date
            ) as load:
                r1 = load.run()
                logger.info("load_incidents_opened finished: %s", r1)

            # task que atualiza por sys_updated_on
            with LoadIncidentsUpdated(
                start_date=start_date, end_date=end_date
            ) as load:
                r2 = load.run()
                logger.info("load_incidents_updated finished: %s", r2)

        except Exception:
            logger.exception("Erro ao executar as pipelines de incidents")
