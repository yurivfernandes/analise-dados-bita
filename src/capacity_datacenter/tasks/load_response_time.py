from datetime import datetime, timedelta
from functools import cached_property
from typing import Dict

import polars as pl
from celery import shared_task
from django.db import connection

from app.utils import MixinGetDataset, Pipeline

from ..models import Node, ResponseTime


class LoadResponseTime(MixinGetDataset, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self, days_back=None):
        """days_back: número de dias para retroceder na consulta.

        Se `days_back` for None, a consulta será executada apenas para o
        antepenúltimo dia (ex: hoje=21/08 -> consultar 19/08).
        """
        super().__init__()
        self.days_back = days_back

    def run(self) -> None:
        """Método principal da classe"""

        self.extract_and_transform_dataset()

        self.load(dataset=self.dataset, model=ResponseTime, filtro={})
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = (
            self.response_time_dataset.with_columns(
                [
                    pl.col("avg_response_time").cast(pl.Float64),
                    pl.col("percent_loss").cast(pl.Float64),
                ]
            )
            .group_by(["node_id", "date"])
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

        # batch node ids to avoid overly long IN lists
        batch_size = 500
        node_batches = [
            self._node_id_list[i : i + batch_size]
            for i in range(0, len(self._node_id_list), batch_size)
        ]
        # determina o intervalo a consultar
        if self.days_back is not None:
            # comportamento padrão: n dias a partir de agora
            days_back = int(self.days_back)
            end_dt = datetime.now()
            start_dt = end_dt - timedelta(days=days_back)
        else:
            # quando days_back não informado, consultar apenas o antepenúltimo dia
            target_day = datetime.now().date() - timedelta(days=4)
            start_dt = datetime(
                target_day.year, target_day.month, target_day.day
            )
            end_dt = start_dt + timedelta(days=3)

        window_start = start_dt
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

        if not collected_rows:
            return pl.DataFrame()

        schema = {
            "NodeID": pl.String,
            "DateTime": pl.String,
            "AvgResponseTime": pl.String,
            "PercentLoss": pl.String,
        }

        return pl.DataFrame(
            data=collected_rows, schema=schema, orient="row"
        ).rename(
            {
                "NodeID": "node_id",
                "DateTime": "date",
                "AvgResponseTime": "avg_response_time",
                "PercentLoss": "percent_loss",
            }
        )

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
def load_response_time_async(_task) -> Dict:
    sync_task = LoadResponseTime()
    return sync_task.run()
