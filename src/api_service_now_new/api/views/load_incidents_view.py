import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...models import ServiceNowExecutionLog
from ...tasks import (
    LoadIncidentSla,
    LoadIncidentsOpened,
    LoadIncidentsUpdated,
    LoadIncidentTask,
    LoadTaskTimeWorked,
)

logger = logging.getLogger(__name__)


def _fmt_hms(td: datetime.timedelta) -> str:
    secs = int(td.total_seconds())
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


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
        started_at = datetime.datetime.now()
        # cria registro de log de execução
        try:
            sd = (
                datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                if isinstance(start_date, str)
                else start_date
            )
        except Exception:
            sd = None
        try:
            ed = (
                datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                if isinstance(end_date, str)
                else end_date
            )
        except Exception:
            ed = None

        exec_log = ServiceNowExecutionLog.objects.create(
            execution_type="incidents",
            start_date=sd,
            end_date=ed,
            started_at=started_at,
            status="running",
        )
        error_message = None
        try:
            # helper de tempo definido no módulo: _fmt_hms

            # task que popula pela data de opened_at (pode deletar+inserir)
            task_name = LoadIncidentsOpened.__name__
            print(f"[{task_name}] Executando ({start_date} -> {end_date})")
            t0 = datetime.datetime.now()
            with LoadIncidentsOpened(
                start_date=start_date, end_date=end_date
            ) as load:
                r1 = load.run()
                logger.info("load_incidents_opened finished: %s", r1)
            print(
                f"[{task_name}] Concluída em {_fmt_hms(datetime.datetime.now() - t0)}"
            )

            # task que atualiza por sys_updated_on
            task_name = LoadIncidentsUpdated.__name__
            print(f"[{task_name}] Executando ({start_date} -> {end_date})")
            t0 = datetime.datetime.now()
            with LoadIncidentsUpdated(
                start_date=start_date, end_date=end_date
            ) as load:
                r2 = load.run()
                logger.info("load_incidents_updated finished: %s", r2)
            print(
                f"[{task_name}] Concluída em {_fmt_hms(datetime.datetime.now() - t0)}"
            )

            # task para incident_sla
            task_name = LoadIncidentSla.__name__
            print(f"[{task_name}] Executando ({start_date} -> {end_date})")
            t1 = datetime.datetime.now()
            with LoadIncidentSla(
                start_date=start_date, end_date=end_date
            ) as load:
                r3 = load.run()
                logger.info("load_incident_sla finished: %s", r3)
            print(
                f"[{task_name}] Concluída em {_fmt_hms(datetime.datetime.now() - t1)}"
            )

            # task para incident_task
            task_name = LoadIncidentTask.__name__
            print(f"[{task_name}] Executando ({start_date} -> {end_date})")
            t2 = datetime.datetime.now()
            with LoadIncidentTask(
                start_date=start_date, end_date=end_date
            ) as load:
                r4 = load.run()
                logger.info("load_incident_task finished: %s", r4)
            print(
                f"[{task_name}] Concluída em {_fmt_hms(datetime.datetime.now() - t2)}"
            )

            # task para task_time_worked
            task_name = LoadTaskTimeWorked.__name__
            print(f"[{task_name}] Executando ({start_date} -> {end_date})")
            t3 = datetime.datetime.now()
            with LoadTaskTimeWorked(
                start_date=start_date, end_date=end_date
            ) as load:
                r5 = load.run()
                logger.info("load_task_time_worked finished: %s", r5)
            print(
                f"[{task_name}] Concluída em {_fmt_hms(datetime.datetime.now() - t3)}"
            )

        except Exception as e:
            logger.exception("Erro ao executar as pipelines de incidents")
            error_message = str(e)
        finally:
            total = datetime.datetime.now() - started_at
            print(
                f"[Thread: {self.__class__.__name__}] Tempo total de execução: {_fmt_hms(total)}",
                flush=True,
            )
            # atualizar log de execução
            try:
                exec_log.ended_at = datetime.datetime.now()
                exec_log.duration_seconds = round(total.total_seconds(), 2)
                exec_log.status = "error" if error_message else "success"
                exec_log.error_message = error_message
                exec_log.save(
                    update_fields=[
                        "ended_at",
                        "duration_seconds",
                        "status",
                        "error_message",
                    ]
                )
            except Exception:
                logger.exception("Falha ao salvar ServiceNowExecutionLog")
