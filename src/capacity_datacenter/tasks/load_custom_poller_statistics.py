from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task
from django.db import connection

from app.utils import MixinGetDataset, Pipeline

from ..models import CustomPollerAssignment, CustomPollerStatistics, Node


class LoadCustompollerStatistics(MixinGetDataset, Pipeline):
    """Classe que busca os dados do custom poller statistics"""

    def __init__(self, days_back=None):
        super().__init__()
        self.days_back = days_back

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()
        self.load(
            dataset=self.dataset, model=CustomPollerStatistics, filtro={}
        )
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = self._custom_poller_statistics_dataset

    @property
    def _custom_poller_statistics_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de Custom Poller Statistics."""

        if not self._assignment_id_list:
            return pl.DataFrame()

        # batch assignment ids
        batch_size = 500
        batches = [
            self._assignment_id_list[i : i + batch_size]
            for i in range(0, len(self._assignment_id_list), batch_size)
        ]

        # periodo
        if self.days_back is not None:
            days_back = int(self.days_back)
            end_dt = datetime.now()
            start_dt = end_dt - timedelta(days=days_back)
        else:
            target_day = datetime.now().date() - timedelta(days=2)
            start_dt = datetime(
                target_day.year, target_day.month, target_day.day
            )
            end_dt = start_dt + timedelta(days=1)

        window_start = start_dt
        collected_rows = []

        while window_start < end_dt:
            window_end = min(window_start + timedelta(hours=2), end_dt)

            for batch in batches:
                in_list = ",".join(f"'{self._esc(a)}'" for a in batch)

                inner_query = (
                    "SELECT\n                        poller.CustomPollerAssignmentID,\n                        poller.NodeID,\n                        poller.RowID,\n                        poller.DateTime,\n                        poller.RawStatus,\n                        poller.Weight\n                    FROM [BR_TD_VITAIT].dbo.[CustomPollerStatistics_CS] poller\n                    WHERE poller.CustomPollerAssignmentID IN ("
                    + in_list
                    + ") AND poller.DateTime >= '"
                    + window_start.strftime("%Y-%m-%d %H:%M:%S")
                    + "' AND poller.DateTime < '"
                    + window_end.strftime("%Y-%m-%d %H:%M:%S")
                    + "'"
                )

                inner_for_openquery = inner_query.replace("'", "''")
                full_query = (
                    "SELECT CustomPollerAssignmentID, NodeID, RowID, DateTime, RawStatus, Weight FROM OPENQUERY([172.21.3.221], '"
                    + inner_for_openquery
                    + "') AS poller"
                )

                with connection.cursor() as cursor:
                    cursor.execute(full_query)
                    result = cursor.fetchall()

                if not result:
                    continue

                for row in result:
                    collected_rows.append(
                        tuple(str(v) if v is not None else None for v in row)
                    )

            window_start = window_end

        if not collected_rows:
            return pl.DataFrame()

        schema = {
            "CustomPollerAssignmentID": pl.String,
            "NodeID": pl.String,
            "RowID": pl.String,
            "DateTime": pl.String,
            "RawStatus": pl.String,
            "Weight": pl.String,
        }

        return (
            pl.DataFrame(data=collected_rows, schema=schema, orient="row")
            .rename(
                {
                    "CustomPollerAssignmentID": "custom_poller_assignment_id",
                    "NodeID": "node_id",
                    "RowID": "row_id",
                    "DateTime": "date",
                    "RawStatus": "raw_status",
                    "Weight": "weight",
                }
            )
            .with_columns(
                [
                    pl.col("weight").cast(pl.Float64),
                ]
            )
            .groupby(["custom_poller_assignment_id", "date"])
            .agg(
                [
                    pl.col("weight").mean().alias("avg_weight"),
                    pl.count().alias("count"),
                ]
            )
            .sort(["custom_poller_assignment_id", "date"])
        )

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
def load_custom_poller_statistics_async(_task) -> Dict:
    sync_task = LoadCustompollerStatistics()
    return sync_task.run()
