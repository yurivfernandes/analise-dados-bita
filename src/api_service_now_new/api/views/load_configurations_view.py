import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...models import ServiceNowExecutionLog
from ...tasks import (
    LoadCmdbCiNetworkLink,
    LoadContractSla,
    LoadGroups,
    LoadSysCompany,
    LoadSysUser,
)

logger = logging.getLogger(__name__)


class LoadConfigurationsView(APIView):
    @staticmethod
    def _fmt_hms(td: datetime.timedelta) -> str:
        secs = int(td.total_seconds())
        h, rem = divmod(secs, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

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
        started_at = datetime.datetime.now()
        # cria registro de log de execução
        results = {}
        errors = []
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
            execution_type="configurations",
            start_date=sd,
            end_date=ed,
            started_at=started_at,
            status="running",
        )
        try:
            # Executar tasks de configuração em paralelo (até N threads)
            tasks_to_run = [
                ("load_contract_sla", LoadContractSla),
                ("load_groups", LoadGroups),
                ("load_sys_company", LoadSysCompany),
                ("load_sys_user", LoadSysUser),
                ("load_cmdb_ci_network_link", LoadCmdbCiNetworkLink),
            ]

            # limitar número de threads simultâneas (pode ajustar conforme necessidade)
            max_threads = 3

            # rodar em lotes de até max_threads
            for i in range(0, len(tasks_to_run), max_threads):
                batch = tasks_to_run[i : i + max_threads]
                threads = []
                for name, cls in batch:
                    th = threading.Thread(
                        target=self._run_task,
                        args=(name, cls, results, errors),
                        daemon=True,
                    )
                    th.start()
                    threads.append(th)
                for th in threads:
                    th.join()

        except Exception:
            logger.exception("Erro ao executar as pipelines de configurations")
        finally:
            total = datetime.datetime.now() - started_at
            print(
                f"[Thread: {self.__class__.__name__}] Tempo total de execução: {self._fmt_hms(total)}",
                flush=True,
            )
            # atualizar log de execução
            try:
                exec_log.ended_at = datetime.datetime.now()
                exec_log.duration_seconds = round(total.total_seconds(), 2)
                exec_log.status = "error" if errors else "success"
                # agrega primeiras mensagens de erro (se houver)
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

    def _run_task(self, task_name, task_cls, results: dict, errors: list):
        """Executa uma task de pipeline em uma thread separada.

        Guarda resultados em `results` e erros em `errors`. Protege contra
        execução duplicada garantindo que `task_name` não esteja presente em `results`.
        """
        # Evitar execução duplicada dentro do mesmo run
        if task_name in results:
            logger.warning(
                "Task %s já foi executada neste run; ignorando segunda execução",
                task_name,
            )
            return

        try:
            print(f"[Configurations] Executando tarefa: {task_name}")
            t0 = datetime.datetime.now()
            with task_cls() as load:
                r = load.run()
                results[task_name] = r
                logger.info("%s finished: %s", task_name, r)
            print(
                f"[Configurations] Concluída: {task_name} em "
                f"{self._fmt_hms(datetime.datetime.now() - t0)}"
            )
        except Exception as e:
            logger.exception("Erro na task %s", task_name)
            errors.append((task_name, str(e)))
