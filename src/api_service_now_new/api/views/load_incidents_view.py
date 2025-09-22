import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...models import ServiceNowExecutionLog
from ...tasks import (
    LoadIncidentSla,
    LoadIncidentSlaUpdated,
    LoadIncidentsOpened,
    LoadIncidentsUpdated,
    LoadIncidentTask,
    LoadIncidentTaskUpdated,
    LoadTaskTimeWorked,
)

logger = logging.getLogger(__name__)


class LoadIncidentsView(APIView):
    @staticmethod
    def _fmt_hms(td: datetime.timedelta) -> str:
        secs = int(td.total_seconds())
        h, rem = divmod(secs, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

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

    def _run_task(
        self, task_name: str, task_cls, start_date, end_date, results, errors
    ):
        """Executa uma task, tentando primeiro com start/end e fazendo fallback se assinatura diferente.

        Tornou-se método de instância para evitar funções aninhadas e permitir testes/override.
        """
        try:
            print(
                f"[Incidents] Executando tarefa: {task_name} ({start_date} -> {end_date})"
            )
            t0 = datetime.datetime.now()
            # Tenta com parâmetros (maioria das tasks de incident usa)
            try:
                with task_cls(
                    start_date=start_date, end_date=end_date
                ) as load:
                    r = load.run()
            except TypeError:
                # fallback se a task não aceita esses kwargs
                with task_cls() as load:
                    r = load.run()
            results[task_name] = r
            print(
                f"[Incidents] Concluída: {task_name} em {self._fmt_hms(datetime.datetime.now() - t0)}"
            )
            logger.info("%s finished: %s", task_name, r)
            return r
        except Exception as e:
            logger.exception("Erro na task %s", task_name)
            errors.append((task_name, str(e)))
            return None

    def _run_pipelines_in_background(self, start_date, end_date):
        """Executa as pipelines de incidents em background com paralelismo controlado.

        Estratégia:
        - Executar simultaneamente (3 threads) as tasks pesadas: opened, updated, incident_sla.
        - Após concluí-las, executar sequencialmente: incident_task, task_time_worked.
        - Registrar tempos, erros e consolidar em ServiceNowExecutionLog.
        """
        started_at = datetime.datetime.now()
        results = {}
        errors = []

        # Parse seguro das datas para log (não quebra se formato inválido)
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

        # método separado para executar uma task; definido como método de instância
        # para evitar funções aninhadas e facilitar testes
        def _run_task_local(name, cls):
            return self._run_task(
                name, cls, start_date, end_date, results, errors
            )

        try:
            # 1. Paralelo: 4 tasks pesadas (construção inicial)
            heavy_tasks = [
                ("load_incidents_opened", LoadIncidentsOpened),
                ("load_incident_sla", LoadIncidentSla),
                ("load_task_time_worked", LoadTaskTimeWorked),
                ("load_incident_task", LoadIncidentTask),
            ]
            threads = []
            for name, cls in heavy_tasks:
                th = threading.Thread(
                    target=_run_task_local, args=(name, cls), daemon=True
                )
                th.start()
                threads.append(th)
            for th in threads:
                th.join()

            # 2. Paralelo: executar updates (atualizações por sys_id) em paralelo
            # update_tasks = [
            #     ("load_incidents_updated", LoadIncidentsUpdated),
            #     ("load_incident_sla_updated", LoadIncidentSlaUpdated),
            #     ("load_incident_task_updated", LoadIncidentTaskUpdated),
            # ]
            # threads = []
            # for name, cls in update_tasks:
            #     th = threading.Thread(
            #         target=_run_task_local, args=(name, cls), daemon=True
            #     )
            #     th.start()
            #     threads.append(th)
            # for th in threads:
            #     th.join()
        except Exception:
            logger.exception("Erro inesperado no pipeline de incidents")
        finally:
            total = datetime.datetime.now() - started_at
            print(
                f"[Thread: {self.__class__.__name__}] Tempo total de execução: {self._fmt_hms(total)}",
                flush=True,
            )
            # Atualiza o log
            try:
                exec_log.ended_at = datetime.datetime.now()
                exec_log.duration_seconds = round(total.total_seconds(), 2)
                exec_log.status = "error" if errors else "success"
                exec_log.error_message = (
                    "; ".join(e for _, e in errors)[:1000] if errors else None
                )
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
