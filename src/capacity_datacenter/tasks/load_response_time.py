from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task
from django.db import connection
from django.utils import timezone as _tz

from app.utils import MixinGetDataset, Pipeline

from ..models import Node, ResponseTime, TaskLog


class LoadResponseTime(MixinGetDataset, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self, start_date=None, end_date=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.log["start_time"] = _tz.now()
        self.log["started_at"] = self.log.get(
            "start_time", self.log.get("started_at")
        )

    def run(self) -> None:
        """Método principal da classe"""

        try:
            self.extract_and_transform_dataset()
            self.load(dataset=self.dataset, model=ResponseTime, filtro=self.date_filter)

        finally:
            self.log["end_time"] = _tz.now()
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
            self.response_time_dataset.group_by(["node_id", "date"])
            .agg(
                [
                    pl.col("avg_response_time")
                    .mean()
                    .round(2)
                    .alias("avg_response_time"),
                    pl.col("percent_loss")
                    .mean()
                    .round(2)
                    .alias("percent_loss"),
                ]
            )
            .sort(["node_id", "date"])
        )

    @property
    def response_time_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de dispositivos Meraki."""

        if not self._node_id_list:
            return pl.DataFrame()

        batch_size = 500
        node_batches = [
            self._node_id_list[i : i + batch_size]
            for i in range(0, len(self._node_id_list), batch_size)
        ]

        window_start, end_dt = self._get_window_range()
        if window_start is None or end_dt is None:
            return pl.DataFrame()

        collected_rows = []

        while window_start < end_dt:
            window_end = min(window_start + timedelta(hours=2), end_dt)

            for batch in node_batches:
                in_list = ",".join(f"'{self._esc(n)}'" for n in batch)

                inner_query = (
                    "SELECT\n                        resp.NodeID,\n                        CONVERT(VARCHAR(10), resp.DateTime, 23) AS DateTime,\n                        resp.AvgResponseTime,\n                        resp.PercentLoss\n                    FROM [BR_TD_VITAIT].dbo.[ResponseTime] resp\n                    WHERE resp.NodeID IN ("
                    + in_list
                    + ") AND resp.DateTime >= '"
                    + window_start.strftime("%Y-%m-%d %H:%M:%S")
                    + "' AND resp.DateTime < '"
                    + window_end.strftime("%Y-%m-%d %H:%M:%S")
                    + "'"
                )
                inner_for_openquery = inner_query.replace("'", "''")
                full_query = (
                    "SELECT NodeID, DateTime, AvgResponseTime, PercentLoss FROM OPENQUERY([172.21.3.221], '"
                    + inner_for_openquery
                    + "') AS resp"
                )

                with connection.cursor() as cursor:
                    cursor.execute(full_query)
                    result = cursor.fetchall()

                if not result:
                    continue

                collected_rows.extend(result)

            window_start = window_end

        self.log["collected_rows_count"] = len(collected_rows)

        if not collected_rows:
            return pl.DataFrame()

        schema = {
            "NodeID": pl.String,
            "DateTime": pl.String,
            "AvgResponseTime": pl.String,
            "PercentLoss": pl.String,
        }

        return (
            pl.DataFrame(data=collected_rows, schema=schema, orient="row")
            .rename(
                {
                    "NodeID": "node_id",
                    "DateTime": "date",
                    "AvgResponseTime": "avg_response_time",
                    "PercentLoss": "percent_loss",
                }
            )
            .with_columns(
                pl.col("avg_response_time").cast(pl.Float64),
                pl.col("percent_loss").cast(pl.Float64),
            )
        )

    def _get_window_range(self):
        """Retorna (start_dt, end_dt) como datetimes para iteração em janelas de 2h.

        Usa `self.start_date` e `self.end_date` (que são objetos date) quando fornecidos.
        Caso não informados, aplica o comportamento anterior (padrão de 3 dias atrás).
        Também define no log `start_range_date` e `end_range_date`.
        """
        if self.start_date is not None and self.end_date is not None:
            # considerar start_date 00:00:00 e end_date até 23:59:59 do dia
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

        # fallback para comportamento antigo
        target_day = datetime.now().date() - timedelta(days=3)
        start_dt = datetime(target_day.year, target_day.month, target_day.day)
        end_dt = start_dt + timedelta(days=2)
        self.log["start_range_date"] = start_dt.date()
        self.log["end_range_date"] = (end_dt - timedelta(seconds=1)).date()
        return start_dt, end_dt

    @property
    def date_filter(self):
        """Retorna o filtro (`dict`) para uso no método `load` com base nas datas recebidas pela view.

        Resultado: {} ou {"date__gte": date, "date__lte": date}
        """
        if self.start_date is None or self.end_date is None:
            # se não informado, tentar usar valores já gravados no log (compat)
            start = self.log.get("start_range_date")
            end = self.log.get("end_range_date")
            if start and end:
                return {"date__gte": start, "date__lte": end}
            return {}
        return {"date__gte": self.start_date, "date__lte": self.end_date}

    @cached_property
    def _node_id_list(self) -> list:
        """Retorna a lista de NodeIDs filtrados por cliente."""
        return list(
            Node.objects.filter(
                nome_do_cliente__icontains="BRADESCO"
            ).values_list("node_id", flat=True)
        )

    def _esc(self, s: str) -> str:
        """Escapa aspas simples para uso em OPENQUERY."""
        return s.replace("'", "''")


@shared_task(
    name="capacity_datacenter.load_response_time_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_response_time_async(_task, start_date=None, end_date=None) -> Dict:
    sync_task = LoadResponseTime(start_date=start_date, end_date=end_date)
    return sync_task.run()
