import os
import re
import time
from functools import cached_property
from typing import Dict

import polars as pl
import requests
from celery import shared_task
from django.db import connection

from app.utils import MixinGetDataset, Pipeline

from ..models import CustomPollerAssignment
from ..utils import MixinQuerys


class LoadCustomPollerAssignment(MixinGetDataset, MixinQuerys, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()
        self.load(
            dataset=self.dataset, model=CustomPollerAssignment, filtro={}
        )
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = self._capacity_dataset

    @property
    def _capacity_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de dispositivos Meraki."""
        query = """
        SELECT
            poller.CustomPollerAssignmentID,
            poller.NodeID
        FROM OPENQUERY(
            [172.21.3.221],
            'SELECT
                poller.CustomPollerAssignmentID,
                poller.NodeID
            FROM [BR_TD_VITAIT].dbo.[CustomPollerAssignment] poller
            LEFT JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
                ON poller.NodeID = nodes.NodeID
            WHERE nodes.Nome_do_cliente like ''%BRADESCO%'''
        ) AS poller
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        if not result:
            return pl.DataFrame()

        data = [
            tuple(str(v) if v is not None else None for v in row)
            for row in result
        ]
        schema = {
            "CustomPollerAssignmentID": pl.String,
            "NodeID": pl.String,
        }

        return pl.DataFrame(data=data, schema=schema, orient="row").rename(
            {
                "CustomPollerAssignmentID": "custom_poller_assignment_id",
                "NodeID": "node_id",
            }
        )


@shared_task(
    name="capacity_datacenter.load_custom_poller_assignment_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_custom_poller_assignment_async(_task) -> Dict:
    sync_task = LoadCustomPollerAssignment()
    return sync_task.run()
