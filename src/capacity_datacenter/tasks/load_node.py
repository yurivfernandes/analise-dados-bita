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

from ..models import Node
from ..utils import MixinQuerys


class LoadNode(MixinGetDataset, MixinQuerys, Pipeline):
    """Classe que busca os dados do Solar"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()

        self.load(dataset=self.dataset, model=Node, filtro={})
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = self._node_dataset

    @property
    def _node_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de Nodes do Solar."""
        query = """
        SELECT
            nodes.Nome_do_Cliente,
            nodes.NodeID,
            nodes.ID_VGR,
            nodes.Caption,
            nodes.Description,
            nodes.Automatizacao,
            nodes.Redundancia
        FROM OPENQUERY(
            [172.21.3.221],
            'SELECT
                nodes.Nome_do_Cliente,
                nodes.NodeID,
                nodes.ID_VGR,
                nodes.Caption,
                nodes.Description,
                nodes.Automatizacao,
                nodes.Redundancia
            FROM [BR_TD_VITAIT].dbo.[Nodes] nodes
            WHERE nodes.Nome_do_cliente like ''%BRADESCO%'''
        ) as nodes
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        # Prepare polars dataframe from rows
        if not result:
            return pl.DataFrame()

        # Build DataFrame using row-orient construction; ensure values are strings where sensible
        data = [
            tuple(str(v) if v is not None else None for v in row)
            for row in result
        ]
        schema = {
            "Nome_do_Cliente": pl.String,
            "NodeID": pl.String,
            "ID_VGR": pl.String,
            "Caption": pl.String,
            "Description": pl.String,
            "Automatizacao": pl.String,
            "Redundancia": pl.String,
        }

        return pl.DataFrame(data=data, schema=schema, orient="row").rename(
            {
                "Nome_do_Cliente": "nome_do_cliente",
                "NodeID": "node_id",
                "ID_VGR": "id_vgr",
                "Caption": "caption",
                "Description": "description",
                "Automatizacao": "automatizacao",
                "Redundancia": "redundancia",
            }
        )


@shared_task(
    name="capacity_datacenter.load_node_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_node_async(_task) -> Dict:
    sync_task = LoadNode()
    return sync_task.run()
