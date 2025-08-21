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

from ..models import Interface


class LoadInterface(MixinGetDataset, Pipeline):
    """Classe que busca os dados do meraki"""

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """Método principal da classe"""
        self.extract_and_transform_dataset()

        self.load(dataset=self.dataset, model=Interface, filtro={})
        return self.log

    def extract_and_transform_dataset(self) -> pl.DataFrame:
        """Extrai e transforma o dataset principal."""
        self.dataset = self.interface_dataset

    @property
    def interface_dataset(self) -> pl.DataFrame:
        """Retorna o dataset de dispositivos Meraki."""
        query = """
        SELECT
            interfaces.NodeId,
            interfaces.InterfaceID,
            interfaces.InterfaceName,
            interfaces.Caption,
            interfaces.ID_VGR
        FROM OPENQUERY(
            [172.21.3.221],
            'SELECT
                interfaces.NodeId,
                interfaces.InterfaceID,
                interfaces.InterfaceName,
                interfaces.Caption,
                interfaces.ID_VGR
            FROM [BR_TD_VITAIT].dbo.[Interfaces] interfaces
            INNER JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
                ON interfaces.NodeID = nodes.NodeID
            WHERE nodes.Nome_do_cliente LIKE ''%BRADESCO%'''
            AND Tipo_Interface = ''WAN''
        ) AS interfaces
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
            "NodeId": pl.String,
            "InterfaceID": pl.String,
            "InterfaceName": pl.String,
            "Caption": pl.String,
            "ID_VGR": pl.String,
        }

        return pl.DataFrame(data=data, schema=schema, orient="row").rename(
            {
                "NodeId": "node_id",
                "InterfaceID": "interface_id",
                "InterfaceName": "interface_name",
                "Caption": "caption",
                "ID_VGR": "id_vgr",
            }
        )



@shared_task(
    name="capacity_datacenter.load_interface_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def load_interface_async(_task) -> Dict:
    sync_task = LoadInterface()
    return sync_task.run()
