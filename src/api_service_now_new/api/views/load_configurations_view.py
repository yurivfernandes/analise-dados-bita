import datetime
import logging
import threading

from rest_framework.response import Response
from rest_framework.views import APIView

from meraki_devices.utils import patch_requests_ssl

from ...models import ServiceNowExecutionLog
from ...tasks import LoadContractSla, LoadGroups, LoadSysCompany, LoadSysUser

logger = logging.getLogger(__name__)


def _fmt_hms(td: datetime.timedelta) -> str:
    secs = int(td.total_seconds())
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


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
            execution_type="configurations",
            start_date=sd,
            end_date=ed,
            started_at=started_at,
            status="running",
        )
        error_message = None
        try:
            # contract_sla
            print("[Configurations] Executando tarefa: load_contract_sla")
            t0 = datetime.datetime.now()
            with LoadContractSla() as load:
                r1 = load.run()
                logger.info("load_contract_sla finished: %s", r1)
            print(
                f"[Configurations] Concluída: load_contract_sla em "
                f"{_fmt_hms(datetime.datetime.now() - t0)}"
            )

            # groups
            print("[Configurations] Executando tarefa: load_groups")
            t1 = datetime.datetime.now()
            with LoadGroups() as load:
                r2 = load.run()
                logger.info("load_groups finished: %s", r2)
            print(
                f"[Configurations] Concluída: load_groups em "
                f"{_fmt_hms(datetime.datetime.now() - t1)}"
            )

            # companies
            print("[Configurations] Executando tarefa: load_sys_company")
            t2 = datetime.datetime.now()
            with LoadSysCompany() as load:
                r3 = load.run()
                logger.info("load_sys_company finished: %s", r3)
            print(
                f"[Configurations] Concluída: load_sys_company em "
                f"{_fmt_hms(datetime.datetime.now() - t2)}"
            )

            # users
            print("[Configurations] Executando tarefa: load_sys_user")
            t3 = datetime.datetime.now()
            with LoadSysUser() as load:
                r4 = load.run()
                logger.info("load_sys_user finished: %s", r4)
            print(
                f"[Configurations] Concluída: load_sys_user em "
                f"{_fmt_hms(datetime.datetime.now() - t3)}"
            )

        except Exception as e:
            logger.exception("Erro ao executar as pipelines de configurations")
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
