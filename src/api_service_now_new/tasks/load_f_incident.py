import re
from typing import Dict, Optional

import polars as pl
from celery import shared_task

from app.utils import MixinGetDataset, Pipeline

from ..models import FIncident, Incident
from ..models.incident_sla import IncidentSla
from ..utils.mixin_querys import MixinQuerys
from ..utils.servicenow import ensure_datetime


class LoadFIncident(MixinGetDataset, Pipeline, MixinQuerys):
    """Lê Incident e IncidentSla do banco, agrega SLAs e salva em incident_with_sla.

    - Filtros (datas) ficam na task
    - Mixin expõe apenas QuerySets base
    - Todas as transformações do SLA ficam na property `_incident_sla`
    """

    def __init__(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ):
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()

    def _normalize_dates(self):
        if not self.start_date or not self.end_date:
            from datetime import datetime, timedelta

            yesterday = (datetime.utcnow() - timedelta(days=1)).date()
            self.start_date = self.start_date or yesterday.isoformat()
            self.end_date = self.end_date or yesterday.isoformat()

    def run(self) -> Dict:
        self._normalize_dates()
        self.extract_and_transform_dataset()
        self.load(
            dataset=self.dataset,
            model=FIncident,
            filtro=self._opened_at_range,
        )
        return self.log

    def extract_and_transform_dataset(self) -> None:
        """Executa todo o fluxo em um único dataset:

        - extrai incidents
        - transforma campos de data e tipos
        - agrega/transforma incident_sla
        - faz join e normaliza colunas finais conforme `FIncident`
        """
        self.dataset = self._incidents.join(
            self._incident_sla,
            left_on="sys_id",
            right_on="task_id",
            how="left",
        ).with_columns(
            pl.col("duracao_sla_atendimento_segundos").cast(pl.Float64),
            pl.col("duracao_sla_resolucao_segundos").cast(pl.Float64),
            pl.when(pl.col("contact_type") == "ALERT")
            .then("PROATIVO")
            .otherwise("REATIVO")
            .alias("tipo_abertura"),
            pl.when(pl.col("parent_incident").is_null())
            .then("PAI")
            .otherwise("FILHO")
            .alias("incidente_pai_ou_filho"),
            pl.col("u_tempo_indisponivel")
            .map_elements(self._parse_period_to_seconds)
            .alias("tempo_indisponivel_segundos"),
            pl.col("time_worked")
            .map_elements(self._parse_period_to_seconds)
            .alias("horas_trabalhadas_segundos"),
            pl.when(
                pl.col("priority").is_in(["1", "1 - Critical", "1 - Crítica"])
            )
            .then("1 - Crítica")
            .when(pl.col("priority").is_in(["2", "2 - High", "2 - Alta"]))
            .then("2 - Alta")
            .when(
                pl.col("priority").is_in(["3", "3 - Moderate", "3 - Moderada"])
            )
            .then("3 - Moderada")
            .when(pl.col("priority").is_in(["4", "4 - Low", "4 - Baixa"]))
            .then("4 - Baixa")
            .when(
                pl.col("priority").is_in(
                    ["5", "5 - Planning", "5 - Planejamento"]
                )
            )
            .then("5 - Planejamento")
            .otherwise(pl.col("priority"))
            .alias("prioridade"),
            pl.col("short_description")
            .map_elements(self._extract_localidade)
            .alias("localidade"),
        )

    @property
    def _incidents(self) -> pl.DataFrame:
        qs = self.get_incident_queryset().filter(**self._opened_at_range)
        field_names = [f.name for f in Incident._meta.fields if f.name != "id"]
        self._incident_ids = list(qs.values_list("sys_id", flat=True))
        schema = {f: pl.Utf8 for f in field_names}
        return pl.DataFrame(data=list(qs.values(*field_names)), schema=schema)

    @property
    def _opened_at_range(self) -> dict:
        """Retorna dicionário para filtro opened_at__range com datas formatadas.

        Exemplo: {'opened_at__range': ['2025-09-30 00:00:00','2025-09-30 23:59:59']}
        """
        # garantir que as datas foram normalizadas antes de construir o range
        self._normalize_dates()
        # mypy/linters: garantir para o analisador que não são None
        assert self.start_date is not None and self.end_date is not None

        return {
            "opened_at__range": [
                ensure_datetime(self.start_date, end=False),
                ensure_datetime(self.end_date, end=True),
            ]
        }

    @property
    def _contract_sla(self) -> pl.DataFrame:
        return pl.DataFrame(
            data=list(
                self.get_contract_sla_queryset().values("sys_id", "sys_name")
            ),
            schema={"sys_id": pl.Utf8, "sys_name": pl.Utf8},
        )

    @property
    def _incident_with_sla_schema(self) -> dict:
        """Schema final: mapeamento final_name -> {{'source': original_col, 'type': polars_type}}"""
        return {
            "id": {"source": "sys_id", "type": pl.Utf8},
            "incidente": {"source": "number", "type": pl.Utf8},
            "data_abertura": {"source": "opened_at", "type": pl.Datetime},
            "data_fechamento": {"source": "closed_at", "type": pl.Datetime},
            "data_fim_da_indisponibilidade": {
                "source": "u_fim_indisponibilidade",
                "type": pl.Datetime,
            },
            "categoria_de_abertura": {"source": "category", "type": pl.Utf8},
            "subcategoria_de_abertura": {
                "source": "subcategory",
                "type": pl.Utf8,
            },
            "detalhe_subcategoria_de_abertura": {
                "source": "u_detail_subcategory",
                "type": pl.Utf8,
            },
            "categoria_da_falha": {
                "source": "u_categoria_da_falha",
                "type": pl.Utf8,
            },
            "subcategoria_da_falha": {
                "source": "u_sub_categoria_da_falha",
                "type": pl.Utf8,
            },
            "detalhe_subcategoria_da_faha": {
                "source": "u_detalhe_sub_categoria_da_falha",
                "type": pl.Utf8,
            },
            "titulo_do_chamado": {
                "source": "short_description",
                "type": pl.Utf8,
            },
            "tipo_do_contato": {"source": "contact_type", "type": pl.Utf8},
            "cmdb_id": {"source": "cmdb_ci", "type": pl.Utf8},
            "status": {"source": "state", "type": pl.Utf8},
            "origem": {"source": "u_origem", "type": pl.Utf8},
            "torre_de_atendimento": {
                "source": "assignment_group_name",
                "type": pl.Utf8,
            },
            "sla_atendimento": {"source": "sla_atendimento", "type": pl.Utf8},
            "sla_resolucao": {"source": "sla_resolucao", "type": pl.Utf8},
            "duracao_sla_atendimento_segundos": {
                "source": "duracao_sla_atendimento_segundos",
                "type": pl.Float64,
            },
            "duracao_sla_resolucao_segundos": {
                "source": "duracao_sla_resolucao_segundos",
                "type": pl.Float64,
            },
            "cliente": {"source": "cliente", "type": pl.Utf8},
            "numero_do_contrato": {
                "source": "contract_number",
                "type": pl.Utf8,
            },
            "localidade": {"source": "localidade", "type": pl.Utf8},
            "tipo_abertura": {"source": "tipo_abertura", "type": pl.Utf8},
            "incidente_pai_ou_filho": {
                "source": "incidente_pai_ou_filho",
                "type": pl.Utf8,
            },
            "tempo_indisponivel_segundos": {
                "source": "tempo_indisponivel_segundos",
                "type": pl.Int64,
            },
            "horas_trabalhadas_segundos": {
                "source": "horas_trabalhadas_segundos",
                "type": pl.Int64,
            },
            "prioridade": {"source": "prioridade", "type": pl.Utf8},
        }

    def _pivot_sla(self, df: pl.DataFrame) -> pl.DataFrame:
        if df.is_empty():
            return df
        df = df.with_columns(
            pl.col("business_duration").cast(pl.Float64),
            pl.col("has_breached"),
            pl.col("task").alias("task_id"),
        )
        nome_col = (
            "contract_sla.sys_name"
            if "contract_sla.sys_name" in df.columns
            else "dv_sla"
        )
        df = df.with_columns(pl.col(nome_col).alias("nome_sla"))
        df = df.filter(
            pl.col("nome_sla").str.contains("SLA Atendimento|SLA Resolução")
        )
        if df.is_empty():
            return df
        df = (
            df.sort(["task_id", "sys_created_on"], reverse=[False, True])
            .groupby(["task_id", "nome_sla"])
            .agg(
                [
                    pl.col("business_duration")
                    .last()
                    .alias("business_duration"),
                    pl.col("has_breached").last().alias("has_breached"),
                ]
            )
            .pivot(
                values=["business_duration", "has_breached"],
                index="task_id",
                columns="nome_sla",
            )
        )
        rename_map = {}
        for c in df.columns:
            if c.startswith("business_duration_"):
                if "SLA Atendimento" in c:
                    rename_map[c] = "duracao_sla_atendimento_segundos"
                elif "SLA Resolução" in c:
                    rename_map[c] = "duracao_sla_resolucao_segundos"
            elif c.startswith("has_breached_"):
                if "SLA Atendimento" in c:
                    rename_map[c] = "sla_atendimento"
                elif "SLA Resolução" in c:
                    rename_map[c] = "sla_resolucao"
        if rename_map:
            df = df.rename(rename_map)
        return df

    @property
    def _incident_sla(self) -> pl.DataFrame:
        field_names = [
            f.name for f in IncidentSla._meta.fields if f.name != "id"
        ]
        qs = (
            self.get_incident_sla_queryset()
            .filter(task__in=self._incident_ids)
            .values(*field_names)
        )

        return (
            pl.DataFrame(qs, schema={f: pl.Utf8 for f in field_names})
            .pipe(self._pivot_sla)
            .join(
                self._contract_sla.select(["sys_id", "sys_name"]).rename(
                    {"sys_id": "sla", "sys_name": "contract_sla.sys_name"}
                ),
                on="sla",
                how="left",
            )
        )

    def _parse_period_to_seconds(self, s: str) -> int:
        if not s:
            return 0
        total = 0
        try:
            m_day = re.search(r"(\d+)\s*Day", s, re.IGNORECASE)
            m_hour = re.search(r"(\d+)\s*Hour", s, re.IGNORECASE)
            m_min = re.search(r"(\d+)\s*Minute", s, re.IGNORECASE)
            m_sec = re.search(r"(\d+)\s*Second", s, re.IGNORECASE)
            if m_day:
                total += int(m_day.group(1)) * 86400
            if m_hour:
                total += int(m_hour.group(1)) * 3600
            if m_min:
                total += int(m_min.group(1)) * 60
            if m_sec:
                total += int(m_sec.group(1))
        except Exception:
            return 0
        return total

    def _extract_localidade(self, s: str) -> Optional[str]:
        if not s:
            return None
        text = str(s)
        if text.upper().startswith("[BRAD") or text.upper().startswith("BRAD"):
            idx = text.find("_")
            if idx > 0:
                start = 1 if text.startswith("[") else 0
                return text[start:idx]
        return None


@shared_task(
    name="api_service_now_new.load_f_incident_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_f_incident_async(
    _task, start_date: Optional[str] = None, end_date: Optional[str] = None
):
    sync_task = LoadFIncident(start_date=start_date, end_date=end_date)
    return sync_task.run()
