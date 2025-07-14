from datetime import datetime, timedelta, timezone
from functools import reduce
from operator import or_
from typing import Dict

import polars as pl

# from celery import shared_task
from django.db.models import Case, Max, Q, QuerySet, Value, When
from django.utils import timezone

from app.utils import MixinGetDataset, Pipeline
from service_now.models import Incident

from ..models import FIncident
from ..utils import MixinQuerys


class LoadIncidentSN(Pipeline, MixinGetDataset, MixinQuerys):
    def __init__(self, full_sync: bool = False):
        self.log = {
            "n_deleted": 0,
            "n_inserted": 0,
            "n_incidents_processed": 0,
        }
        self.full_sync = full_sync

    def get_incident_queryset(self) -> QuerySet:
        """Retorna o Queryset com os dados de Incidentes do Service Now"""
        if self.full_sync == False:
            ten_days_ago = timezone.now() - timedelta(days=10)
            return (
                super()
                .get_incident_queryset()
                .filter(**self._filtro_incident, closed_at__gte=ten_days_ago)
            )
        return (super().get_incident_queryset()).filter(*self._filtro_incident)

    def get_incident_sla_queryset(self) -> QuerySet:
        """Retorna o Queryset com os dados de SLA dos Incidentes do Service Now"""
        return (
            super()
            .get_incident_sla_queryset()
            .filter(**self._filtro_incident_sla)
        )

    @property
    def _filtro_incident(self) -> dict:
        return {}

    @property
    def _filtro_incident_sla(self) -> dict:
        return {}

    def run(self) -> dict:
        print(f"...INICIANDO A TASK [{self.__class__.__name__}]...")
        self._extract_and_transform_dataset()
        self.load(
            dataset=self.dataset, model=FIncident, filtro=self._filtro_incident
        )
        return self.log

    def _extract_and_transform_dataset(self) -> None:
        """Extrai e transforma os dados do ServiceNow usando Polars"""
        self.dataset = (
            self._incidents_dataset.pipe(self.convert_datetime_columns)
            .pipe(self._handle_duplicates)
            .pipe(self.join_sla_dataset)
        )

    @property
    def _incidents_dataset(self) -> pl.DataFrame:
        """Retorna o DataSet de incidentes do Service Now."""
        schema = self.generate_schema_from_model(model=Incident)
        schema_fincident = self.generate_schema_from_model(model=FIncident)
        schema_string = {
            key: {
                "rename": schema_fincident[key].get("rename"),
                "type": pl.String,
            }
            for key in schema_fincident
            if key in schema and key != "id"
        }
        query_set = self.stringify_all_values(
            list(self.get_incident_queryset().values(*schema_string.keys()))
        )

        return self.get_dataset(
            query_set=query_set,
            schema=schema_string,
        )

    def stringify_all_values(self, data: list[dict]) -> list[dict]:
        """Converte todos os valores de todos os registros para string"""
        for item in data:
            for key, value in item.items():
                try:
                    if isinstance(value, datetime):
                        # Remove tzinfo se necessário e formata como ISO
                        value = value.replace(tzinfo=None).isoformat(sep=" ")
                    item[key] = str(value) if value is not None else ""
                except Exception:
                    item[key] = ""
        return data

    def _handle_duplicates(self, df: pl.DataFrame) -> pl.DataFrame:
        """
        Trata incidentes duplicados mantendo os encerrados ou o primeiro encontrado.
        """
        # Criando coluna para priorização (1 para encerrados, 0 para outros)
        df_with_priority = df.with_columns(
            pl.when(pl.col("state").is_in([6, 7]))
            .then(1)
            .otherwise(0)
            .alias("priority")
        )

        # Ordenando por number e priority (descendente) e pegando o primeiro de cada grupo
        return (
            df_with_priority.sort(
                ["number", "priority"], descending=[False, True]
            )
            .groupby("number", maintain_order=True)
            .first()
        )

    def convert_datetime_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Converte as colunas de datetime necessárias no dataset."""
        return df.with_columns(
            pl.col("opened_at")
            .cast(pl.Datetime, strict=False)
            .alias("opened_at"),
            pl.col("closed_at")
            .cast(pl.Datetime, strict=False)
            .alias("closed_at"),
            pl.col("resolved_at")
            .cast(pl.Datetime, strict=False)
            .alias("resolved_at"),
            pl.col("u_data_normalizacao_servico")
            .cast(pl.Datetime, strict=False)
            .alias("u_data_normalizacao_servico"),
            pl.col("u_tempo_indisponivel")
            .cast(pl.Datetime, strict=False)
            .alias("u_tempo_indisponivel"),
        )

    def join_sla_dataset(self, df: pl.DataFrame) -> pl.DataFrame:
        """Busca o SLA com base nos tickets do DF principal."""

        schema = {
            "task": pl.String,
            "dv_sla_atendimento": pl.String,
            "dv_sla_resolucao": pl.String,
            "sla_first": pl.String,
            "sla_resolved": pl.String,
        }
        sys_id_list = [
            str(sys_id)
            for sys_id in df["sys_id"].unique()
            if sys_id not in [None, "", "None", "Null", "none", "null"]
        ]

        sla_keywords = [
            "[VITA] FIRST",
            "[VITA] RESOLVED",
            "[VGR] SLA Atendimento",
            "[VGR] SLA Resolução",
        ]
        atendimento_cases = [
            When(
                dv_sla__icontains=kw,
                then=Case(
                    When(has_breached=True, then=Value(True)),
                    default=Value(False),
                ),
            )
            for kw in sla_keywords
            if any(term in kw.lower() for term in ["first", "atendimento"])
        ]

        resolucao_cases = [
            When(
                dv_sla__icontains=kw,
                then=Case(
                    When(has_breached=True, then=Value(True)),
                    default=Value(False),
                ),
            )
            for kw in sla_keywords
            if any(term in kw.lower() for term in ["resolved", "resolução"])
        ]

        sla_first_cases = [
            When(dv_sla__icontains=kw, then=Value(kw))
            for kw in sla_keywords
            if any(term in kw.lower() for term in ["first", "atendimento"])
        ]

        sla_resolved_cases = [
            When(dv_sla__icontains=kw, then=Value(kw))
            for kw in sla_keywords
            if any(term in kw.lower() for term in ["resolved", "resolução"])
        ]

        query_set = (
            self.get_incident_sla_queryset()
            .filter(task__in=sys_id_list)
            .filter(
                reduce(or_, (Q(dv_sla__icontains=kw) for kw in sla_keywords))
            )
            .values("task")
            .annotate(
                dv_sla_atendimento=Max(
                    Case(*atendimento_cases, default=Value(None))
                ),
                dv_sla_resolucao=Max(
                    Case(*resolucao_cases, default=Value(None))
                ),
                sla_first=Max(Case(*sla_first_cases, default=Value(None))),
                sla_resolved=Max(
                    Case(*sla_resolved_cases, default=Value(None))
                ),
            )
        )

        df_sla = pl.DataFrame(
            data=list(query_set),
            schema=schema,
        ).rename({"task": "sys_id"})
        return df.join(
            df_sla,
            on="sys_id",
            how="left",
        )


# @shared_task(
#     name="dw_analytics.load_incidents_sn",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_incident_sn_async(self, full_sync: bool = False) -> Dict:
    sync_task = LoadIncidentSN(full_sync=full_sync)
    return sync_task.run()
