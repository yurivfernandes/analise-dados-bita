from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task
from django.db import connection
from django.utils import timezone

from app.utils import MixinGetDataset, Pipeline

from ..models import (
    CustomPollerAssignment,
    CustomPollerStatistics,
    Node,
    TaskLog,
)


class LoadCustompollerStatistics(MixinGetDataset, Pipeline):
    """Classe que busca os dados do custom poller statistics"""

    def __init__(self, start_date=None, end_date=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.log["start_time"] = timezone.now()
        self.log["started_at"] = self.log.get(
            "start_time", self.log.get("started_at")
        )

    def run(self) -> Dict:
        """Método principal da classe"""
        try:
            self.extract_and_transform_dataset()
            self.load(
                dataset=self.dataset,
                model=CustomPollerStatistics,
                filtro=self._filter,
            )
        finally:
            self.log["end_time"] = timezone.now()
            self.log["finished_at"] = self.log.get(
                "end_time", self.log.get("finished_at")
            )
            start = self.log.get("start_time") or self.log.get("started_at")
            end = self.log.get("end_time") or self.log.get("finished_at")
            if start and end:
                self.log["duration_seconds"] = round(
                    (end - start).total_seconds(), 2
                )
                self.log["duration"] = self.log["duration_seconds"]
            else:
                self.log["duration_seconds"] = None

        serializable_log = {}
        for k, v in self.log.items():
            try:
                if hasattr(v, "isoformat"):
                    serializable_log[k] = v.isoformat()
                else:
                    serializable_log[k] = v
            except (AttributeError, TypeError, ValueError):
                serializable_log[k] = str(v)
        self.log["transformed_rows_count"] = len(self.dataset)
        TaskLog.objects.create(
            task_name=self.__class__.__name__,
            run_at=self.log.get("start_time"),
            log=serializable_log,
        )

        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = (
            self._custom_poller_statistics_dataset.with_columns(
                pl.col("weight").cast(pl.Float64),
                pl.col("raw_status").cast(pl.Float64),
                pl.col("date").cast(pl.Date),
            )
            .group_by(["node_id", "date"])
            .agg(
                [
                    pl.col("weight").mean().round(2).alias("weight"),
                    pl.col("raw_status").mean().round(2).alias("raw_status"),
                ]
            )
            .sort(["node_id", "date"])
        )

    @property
    def _custom_poller_statistics_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de Custom Poller Statistics."""

        if not self._assignment_id_list:
            return pl.DataFrame()

        batch_size = 180
        batches = [
            self._assignment_id_list[i : i + batch_size]
            for i in range(0, len(self._assignment_id_list), batch_size)
        ]

        window_start, end_dt = self._get_window_range()
        if window_start is None or end_dt is None:
            return pl.DataFrame()
        collected_rows = []

        while window_start < end_dt:
            window_end = min(window_start + timedelta(hours=2), end_dt)

            for batch in batches:
                in_list = ",".join(f"'{self._esc(a)}'" for a in batch)

                inner_query = (
                    "SELECT\n                        poller.CustomPollerAssignmentID,\n                        poller.RowID,\n                        CONVERT(VARCHAR(10), poller.DateTime, 23) AS DateTime,\n                        poller.RawStatus,\n                        poller.Weight\n                    FROM [BR_TD_VITAIT].dbo.[CustomPollerStatistics_CS] poller\n                    WHERE poller.CustomPollerAssignmentID IN ("
                    + in_list
                    + ") AND poller.DateTime >= '"
                    + window_start.strftime("%Y-%m-%d %H:%M:%S")
                    + "' AND poller.DateTime < '"
                    + window_end.strftime("%Y-%m-%d %H:%M:%S")
                    + "'"
                )

                inner_for_openquery = inner_query.replace("'", "''")
                full_query = (
                    "SELECT CustomPollerAssignmentID,  RowID, DateTime, RawStatus, Weight FROM OPENQUERY([172.21.3.221], '"
                    + inner_for_openquery
                    + "') AS poller"
                )

                with connection.cursor() as cursor:
                    cursor.execute(full_query)
                    result = cursor.fetchall()

                if not result:
                    continue

                collected_rows.extend(result)

            print(f"Tamanho do dataset:{len(collected_rows)}")
            window_start = window_end
        print(
            f"Tamanho final do dataset antes de agrupar:{len(collected_rows)}"
        )
        self.log["collected_rows_count"] = len(collected_rows)
        if not collected_rows:
            return pl.DataFrame()

        schema = {
            "CustomPollerAssignmentID": pl.String,
            "RowID": pl.String,
            "DateTime": pl.String,
            "RawStatus": pl.String,
            "Weight": pl.String,
        }

        return (
            pl.DataFrame(data=collected_rows, schema=schema, orient="row")
            .with_columns(
                pl.col("CustomPollerAssignmentID")
                .replace(self._assignment_id_map)
                .alias("node_id")
            )
            .rename(
                {
                    "RowID": "row_id",
                    "DateTime": "date",
                    "RawStatus": "raw_status",
                    "Weight": "weight",
                }
            )
            .select(["node_id", "row_id", "date", "raw_status", "weight"])
        )

    def _get_window_range(self):
        """Retorna (start_dt, end_dt) como datetimes para iteração em janelas de 2h.

        Usa `self.start_date` e `self.end_date` (objetos date) quando fornecidos.
        Caso não informados, aplica o comportamento anterior (padrão de 2 dias atrás).
        Também define no log `start_range_date` e `end_range_date`.
        """
        if self.start_date is not None and self.end_date is not None:
            start_dt = datetime(
                self.start_date.year,
                self.start_date.month,
                self.start_date.day,
            )
            end_dt = datetime(
                self.end_date.year, self.end_date.month, self.end_date.day
            ) + timedelta(days=1)
            self.log["start_range_date"] = start_dt.date()
            self.log["end_range_date"] = (end_dt - timedelta(seconds=1)).date()
            return start_dt, end_dt

        target_day = datetime.now().date() - timedelta(days=2)
        start_dt = datetime(target_day.year, target_day.month, target_day.day)
        end_dt = start_dt + timedelta(days=1)
        self.log["start_range_date"] = start_dt.date()
        self.log["end_range_date"] = (end_dt - timedelta(seconds=1)).date()
        return start_dt, end_dt

    @property
    def _filter(self):
        """Retorna o filtro (`dict`) para uso no método `load` com base nas datas recebidas pela view.

        Resultado: {} ou {"date__gte": date, "date__lte": date}
        """
        if self.start_date is None or self.end_date is None:
            start = self.log.get("start_range_date")
            end = self.log.get("end_range_date")
            if start and end:
                return {"date__gte": start, "date__lte": end}
            return {}
        return {"date__gte": self.start_date, "date__lte": self.end_date}

    @cached_property
    def _assignment_id_map(self) -> dict:
        """Retorna um dicionário {assignment_id: node_id} filtrado por cliente (BRADESCO)."""
        if not self._node_id_list:
            return {}
        batch_size = 500
        mapping = {}
        for i in range(0, len(self._node_id_list), batch_size):
            batch = self._node_id_list[i : i + batch_size]
            qs = CustomPollerAssignment.objects.filter(
                node_id__in=batch
            ).values_list("custom_poller_assignment_id", "node_id")
            for aid, node in qs:
                if aid is not None:
                    mapping[str(aid)] = node
        return mapping

    @cached_property
    def _assignment_id_list(self) -> list:
        """Retorna a lista de CustomPollerAssignmentIDs filtrados por cliente (BRADESCO)."""
        if not self._node_id_list:
            return []
        batch_size = 500
        assignment_ids = []
        for i in range(0, len(self._node_id_list), batch_size):
            batch = self._node_id_list[i : i + batch_size]
            qs = CustomPollerAssignment.objects.filter(
                node_id__in=batch
            ).values_list("custom_poller_assignment_id", flat=True)
            assignment_ids.extend(list(qs))
        return list(dict.fromkeys(assignment_ids))

    @cached_property
    def _node_id_list(self) -> list:
        """Lista de node_id's do cliente BRADESCO (cached)."""
        return list(
            Node.objects.filter(
                nome_do_cliente__icontains="BRADESCO"
            ).values_list("node_id", flat=True)
        )

    def _esc(self, s: str) -> str:
        """Escapa aspas simples para uso em OPENQUERY."""
        return s.replace("'", "''")


@shared_task(
    name="capacity_datacenter.load_custom_poller_statistics_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_custom_poller_statistics_async(
    _task, start_date=None, end_date=None
) -> Dict:
    sync_task = LoadCustompollerStatistics(
        start_date=start_date, end_date=end_date
    )
    return sync_task.run()
