from functools import cached_property

import polars as pl

# from celery import shared_task
from django.db import connection

from app.utils.pipeline import Pipeline

from ..models import SolarNodeOriginal
from ..utils import MixinTasksSolar


class LoadNodeOriginalVGR(MixinTasksSolar, Pipeline):
    """Extrai e carrega os dados dos Nodes."""

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.company_remedy_list = kwargs.get("company_remedy_list")
        self.nome_cliente_list = kwargs.get("nome_do_cliente_list")

    @property
    def _filtro(self) -> dict:
        if (
            len(self.company_remedy_list) > 0
            and len(self.nome_cliente_list) > 0
        ):
            return {
                "company_remedy__in": self.company_remedy_list,
                "nome_cliente__in": self.nome_cliente_list,
            }
        if len(self.company_remedy_list) > 0:
            return {"company_remedy__in": self.company_remedy_list}
        if len(self.nome_cliente_list) > 0:
            return {
                "nome_cliente__in": self.nome_cliente_list,
            }
        return {}

    @cached_property
    def _schema_query_node(self) -> dict:
        """Busca o schema a ser utilizado no dataset"""
        return {
            "nodes.Nome_do_cliente": {
                "rename": "nome_cliente",
                "dtype": pl.String,
            },
            "nodes.Company_Remedy": {
                "rename": "company_remedy",
                "dtype": pl.String,
            },
            "nodes.GRUPO_CORPORATIVO": {
                "rename": "grupo_corporativo",
                "dtype": pl.String,
            },
            "nodes.ID_VGR": {"rename": "id_vgr", "dtype": pl.String},
            "nodes.DESIGNADOR": {"rename": "designador", "dtype": pl.String},
            "nodes.Operadora": {"rename": "operadora", "dtype": pl.String},
            "nodes.Tecnologia": {"rename": "tecnologia", "dtype": pl.String},
            "SAE.cep": {"rename": "cep", "dtype": pl.String},
            "nodes.RAZAO_SOCIAL": {
                "rename": "razao_social",
                "dtype": pl.String,
            },
            "nodes.NodeID": {"rename": "node_id", "dtype": pl.String},
            "nodes.Description": {"rename": "description", "dtype": pl.String},
            "nodes.IP_Address": {"rename": "ip_node", "dtype": pl.String},
            "nodes.Caption": {"rename": "caption", "dtype": pl.String},
            "SAE.status_vantive": {
                "rename": "status_vantive",
                "dtype": pl.String,
            },
            "SAE.velocidade": {"rename": "velocidade", "dtype": pl.String},
        }

    def run(self) -> dict:
        print(f"...INICIANDO A TASK [{self.__class__.__name__}]...")
        dataset = self._node_dataset
        print("...DATASET PRONTO PARA SER INSERIDO NO BANCO!...")
        self.load(dataset=dataset, model=SolarNodeOriginal)
        print("...DADOS SALVOS NO BANCO, FINALIZANDO...")
        return self.log

    @property
    def _node_dataset(self) -> pl.DataFrame:
        """Executa a query para buscar todas os Nodes no banco de dados."""
        query = """
            SELECT 
                node.Nome_do_cliente,
                node.Company_Remedy,
                node.GRUPO_CORPORATIVO,
                node.ID_VGR,
                node.DESIGNADOR,
                node.Operadora,
                node.Tecnologia,
                SAE.cep,
                node.RAZAO_SOCIAL,
                node.NodeID,
                node.Description,
                node.IP_Address,
                node.Caption,
                SAE.status_vantive,
                SAE.velocidade
            FROM OPENQUERY ([172.21.3.221],    
                'SELECT
                        nodes.Nome_do_cliente
                        ,nodes.Company_Remedy
                        ,nodes.GRUPO_CORPORATIVO
                        ,nodes.ID_VGR
                        ,nodes.DESIGNADOR
                        ,nodes.Operadora
                        ,nodes.Tecnologia
                        ,nodes.RAZAO_SOCIAL
                        ,nodes.NodeID
                        ,nodes.Description
                        ,nodes.IP_Address
                        ,nodes.Caption
                    FROM [BR_TD_VITAIT].dbo.[nodes] nodes
                    where
                    ( nodes.Operação  IN (
                    ''SDWAN CLIENTES''
                    ,''BRADESCO VGR''
                    ,''FLEURY''
                    )
                    OR nodes.OPERAÇÃO  = ''TI'' 
                    AND Company_Remedy LIKE (''%ARCOS DOURADOS%'')
                    )
                    OR nodes.OPERAÇÃO_VITA = ''VIVO VITA''
                ') AS node
                LEFT JOIN OPENQUERY(
                    [10.128.223.125],
                    'SELECT
                        ID_VANTIVE	as id_vantive,					
                        VELOCIDADE as velocidade,
                        STATUS_VANTIVE as status_vantive,
                        CEP as cep
                    FROM  
                        LK_RELATORIO_12.SAE.SAE.TB_PEDIDOS_DADOS with (nolock)
                        WHERE
                        SERVICO IN (''VIVO GESTÃO DE REDES'')
                    ') AS SAE  
                    ON CAST(SAE.ID_VANTIVE AS VARCHAR) = CAST(node.ID_VGR AS VARCHAR)
            """
        print("...EXECUTANDO A QUERY PRINCIPAL...")
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pl.DataFrame(
            data=[tuple(str(value) for value in row) for row in result],
            schema=dict(
                **{
                    k: v.get("type")
                    for k, v in self._schema_query_node.items()
                }
            ),
            orient="row",
        ).rename({k: v["rename"] for k, v in self._schema_query_node.items()})


# @shared_task(
#     name="receita.load_consolidacao",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_node_original_vgr_async(self, filtros: dict) -> dict:
    with LoadNodeOriginalVGR(**filtros) as task:
        log = task.run()
    return log
