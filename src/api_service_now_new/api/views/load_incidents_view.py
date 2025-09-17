import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...tasks import (
    LoadIncidentSla,
    LoadIncidentsOpened,
    LoadIncidentTask,
    LoadTaskTimeWorked,
)

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
            started_at = datetime.datetime.now()

            # task que popula pela data de opened_at (pode deletar+inserir)
            print(
                f"[Incidents] Executando tarefa: load_incidents_opened ({start_date} -> {end_date})"
            )
            t0 = datetime.datetime.now()
            with LoadIncidentsOpened(
                start_date=start_date, end_date=end_date
            ) as load:
                r1 = load.run()
                logger.info("load_incidents_opened finished: %s", r1)
            print(
                f"[Incidents] Concluída: load_incidents_opened em "
                f"{(datetime.datetime.now() - t0).total_seconds():.2f}s"
            )

            # task que atualiza por sys_updated_on
            # with LoadIncidentsUpdated(
            #     start_date=start_date, end_date=end_date
            # ) as load:
            #     r2 = load.run()
            #     logger.info("load_incidents_updated finished: %s", r2)

            # task para incident_sla
            print(
                f"[Incidents] Executando tarefa: load_incident_sla ({start_date} -> {end_date})"
            )
            t1 = datetime.datetime.now()
            with LoadIncidentSla(
                start_date=start_date, end_date=end_date
            ) as load:
                r3 = load.run()
                logger.info("load_incident_sla finished: %s", r3)
            print(
                f"[Incidents] Concluída: load_incident_sla em "
                f"{(datetime.datetime.now() - t1).total_seconds():.2f}s"
            )

            # task para incident_task
            print(
                f"[Incidents] Executando tarefa: load_incident_task ({start_date} -> {end_date})"
            )
            t2 = datetime.datetime.now()
            with LoadIncidentTask(
                start_date=start_date, end_date=end_date
            ) as load:
                r4 = load.run()
                logger.info("load_incident_task finished: %s", r4)
            print(
                f"[Incidents] Concluída: load_incident_task em "
                f"{(datetime.datetime.now() - t2).total_seconds():.2f}s"
            )

            # task para task_time_worked
            print(
                f"[Incidents] Executando tarefa: load_task_time_worked ({start_date} -> {end_date})"
            )
            t3 = datetime.datetime.now()
            with LoadTaskTimeWorked(
                start_date=start_date, end_date=end_date
            ) as load:
                r5 = load.run()
                logger.info("load_task_time_worked finished: %s", r5)
            print(
                f"[Incidents] Concluída: load_task_time_worked em "
                f"{(datetime.datetime.now() - t3).total_seconds():.2f}s"
            )

            total = (datetime.datetime.now() - started_at).total_seconds()
            print(f"[Incidents] Tempo total de execução: {total:.2f}s")

        except Exception:
            logger.exception("Erro ao executar as pipelines de incidents")
