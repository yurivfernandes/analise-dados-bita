from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task
from django.db import connection
from django.utils import timezone as _tz

from app.utils import MixinGetDataset, Pipeline

from ..models import Node, InterfaceTraffic, TaskLog


class LoadInterfaceTraffic(MixinGetDataset, Pipeline):
    """Carrega dados de tráfego das interfaces a partir da base remota."""

    def __init__(self, start_date=None, end_date=None):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.log["start_time"] = _tz.now()
        self.log["started_at"] = self.log.get(
            "start_time", self.log.get("started_at")
        )

    def run(self) -> None:
        try:
            self.extract_and_transform_dataset()
            self.load(dataset=self.dataset, model=InterfaceTraffic, filtro=self.date_filter)

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
        self.dataset = (
            self.interface_traffic_dataset.group_by(["node_id", "date"]) 
            .agg([
                pl.col("in_average_bps").mean().round(2).alias("in_average_bps"),
                pl.col("out_average_bps").mean().round(2).alias("out_average_bps"),
            ])
            .sort(["node_id", "date"])
        )

    @property
    def interface_traffic_dataset(self) -> pl.DataFrame:
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
                    "SELECT\n                        traffic.NodeID,\n                        CONVERT(VARCHAR(10), traffic.DateTime, 23) AS DateTime,\n                        traffic.In_Averagebps,\n                        traffic.Out_Averagebps\n                    FROM [BR_TD_VITAIT].dbo.[InterfaceTraffic] traffic\n                    WHERE traffic.NodeID IN ("
                    + in_list
                    + ") AND traffic.DateTime >= '"
                    + window_start.strftime("%Y-%m-%d %H:%M:%S")
                    + "' AND traffic.DateTime < '"
                    + window_end.strftime("%Y-%m-%d %H:%M:%S")
                    + "'"
                )
                inner_for_openquery = inner_query.replace("'", "''")
                full_query = (
                    "SELECT NodeID, DateTime, In_Averagebps, Out_Averagebps FROM OPENQUERY([172.21.3.221], '"
                    + inner_for_openquery
                    + "') AS traffic"
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
            "In_Averagebps": pl.String,
            "Out_Averagebps": pl.String,
        }

        return (
            pl.DataFrame(data=collected_rows, schema=schema, orient="row")
            .rename(
                {
                    "NodeID": "node_id",
                    "DateTime": "date",
                    "In_Averagebps": "in_average_bps",
                    "Out_Averagebps": "out_average_bps",
                }
            )
            .with_columns(
                pl.col("in_average_bps").cast(pl.Float64),
                pl.col("out_average_bps").cast(pl.Float64),
            )
        )

    def _get_window_range(self):
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

        target_day = datetime.now().date() - timedelta(days=3)
        start_dt = datetime(target_day.year, target_day.month, target_day.day)
        end_dt = start_dt + timedelta(days=2)
        self.log["start_range_date"] = start_dt.date()
        self.log["end_range_date"] = (end_dt - timedelta(seconds=1)).date()
        return start_dt, end_dt

    @property
    def date_filter(self):
        if self.start_date is None or self.end_date is None:
            start = self.log.get("start_range_date")
            end = self.log.get("end_range_date")
            if start and end:
                return {"date__gte": start, "date__lte": end}
            return {}
        return {"date__gte": self.start_date, "date__lte": self.end_date}

    @cached_property
    def _node_id_list(self) -> list:
        return list(
            Node.objects.filter(
                nome_do_cliente__icontains="BRADESCO"
            ).values_list("node_id", flat=True)
        )

    def _esc(self, s: str) -> str:
        return s.replace("'", "''")


@shared_task(
    name="capacity_datacenter.load_interface_traffic_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_interface_traffic_async(_task, start_date=None, end_date=None) -> Dict:
    sync_task = LoadInterfaceTraffic(start_date=start_date, end_date=end_date)
    return sync_task.run()
