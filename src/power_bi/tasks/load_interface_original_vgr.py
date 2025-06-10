from functools import cached_property

import polars as pl

# from celery import shared_task
from django.db import connection, transaction

from app.utils.pipeline import Pipeline

from ..models import SolarInterfaceOriginal
from ..utils.mixin import MixinViews


class LoadInterfaceOriginalVGR(MixinViews, Pipeline):
    """Extrai, transforma e carrega os dados Interface"""

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
    def _schema_query_interfaces(self) -> dict:
        """Busca o schema a ser utilizado no dataset"""
        return {
            "N.Nome_do_cliente": {
                "rename": "nome_cliente",
                "dtype": pl.String,
            },
            "N.Company_Remedy": {
                "rename": "company_remedy",
                "dtype": pl.String,
            },
            "N.RAZAO_SOCIAL": {"rename": "razao_social", "dtype": pl.String},
            "N.GRUPO_CORPORATIVO": {
                "rename": "grupo_corporativo",
                "dtype": pl.String,
            },
            "N.ID_VGR": {"rename": "id_vgr", "dtype": pl.String},
            "N.DESIGNADOR": {"rename": "designador", "dtype": pl.String},
            "N.Operadora": {"rename": "operadora", "dtype": pl.String},
            "SAE.NOME_OPERADORA": {
                "rename": "nome_operadora",
                "dtype": pl.String,
            },
            "SAE.NOME_OPERADORA_ATUAL": {
                "rename": "nome_operadora_atual",
                "dtype": pl.String,
            },
            "N.Tecnologia": {"rename": "tecnologia", "dtype": pl.String},
            "N.CEP": {"rename": "cep", "dtype": pl.String},
            "SAE.VELOCIDADE": {"rename": "velocidade", "dtype": pl.String},
            "N.Banda_Contratada_Entrada": {
                "rename": "banda_contratada_entrada",
                "dtype": pl.String,
            },
            "SAE.STATUS_VANTIVE": {
                "rename": "status_vantive",
                "dtype": pl.String,
            },
            "N.INTERFACEID": {"rename": "interface_id", "dtype": pl.String},
            "N.IP_Device": {"rename": "ip_interface", "dtype": pl.String},
            "N.IP_Address": {"rename": "ip_node", "dtype": pl.String},
            "N.Description": {"rename": "description", "dtype": pl.String},
            "InterfaceName": {"rename": "interface_name", "dtype": pl.String},
            "Caption": {"rename": "caption", "dtype": pl.String},
            "Nome_da_Interface": {
                "rename": "nome_interface",
                "dtype": pl.String,
            },
        }

    def run(self) -> dict:
        print("Iniciando...")
        self.dataset = self._interface_dataset
        print("Dataset pronto para ser carregado...")
        self.load()
        print("Finalizando...")
        return self.log

    @property
    def _interface_dataset(self) -> pl.DataFrame:
        """Executa a query para buscar todas as interfaces no banco de dados."""
        query = """
        SELECT 
            N.Company_Remedy,
            N.Nome_do_cliente,
            N.RAZAO_SOCIAL,
            N.GRUPO_CORPORATIVO,
            N.ID_VGR,
            N.DESIGNADOR,
            N.Operadora,
            SAE.NOME_OPERADORA,
            SAE.NOME_OPERADORA_ATUAL,
            N.Tecnologia,
            N.CEP,
            SAE.VELOCIDADE,
            N.Banda_Contratada_Entrada,
            SAE.STATUS_VANTIVE,
            N.INTERFACEID,
            N.IP_Device,
            N.IP_Address,
            N.Description,
            InterfaceName,
            Caption,
            Nome_da_Interface
        FROM OPENQUERY ([172.21.3.221],     
                'SELECT
                        I.Nome_do_cliente,
                        nodes.Company_Remedy,
                        I.GRUPO_CORPORATIVO,
                        I.ID_VGR,
                        I.DESIGNADOR,
                        I.Operadora,
                        I.Tecnologia,
                        I.CEP,
                        I.RAZAO_SOCIAL,
                        I.Banda_Contratada_Entrada,
                        I.INTERFACEID,
                        I.IP_Device,
                        nodes.Description,
                        nodes.IP_Address,
                        I.InterfaceName,
                        I.Caption,
                        I.Nome_da_Interface
                    FROM [BR_TD_VITAIT].dbo.[Nodes] nodes
                        INNER JOIN [BR_TD_VITAIT].dbo.[INTERFACES] I ON I.NodeID = nodes.NodeID
                    where
                    ( 
                        nodes.Operação  IN (''SDWAN CLIENTES'',''BRADESCO VGR'',''FLEURY'') 
                        OR nodes.OPERAÇÃO  = ''TI''  
                        AND Company_Remedy LIKE (''%ARCOS DOURADOS%'')
                    )
                    OR I.OPERAÇÃO_VITA = ''VIVO VITA''
                    ') AS N 
                    LEFT JOIN  OPENQUERY(
                        [10.128.223.125],
                        'SELECT
                            ID_VANTIVE	as id_vantive,					
                            VELOCIDADE as velocidade,
                            STATUS_VANTIVE as status_vantive,
                            CEP as cep,
                            NOME_OPERADORA as nome_operadora,
                            NOME_OPERADORA_ATUAL as nome_operadora_atual
                        FROM  
                            LK_RELATORIO_12.SAE.SAE.TB_PEDIDOS_DADOS with (nolock)
                            WHERE
                            SERVICO IN (''VIVO GESTÃO DE REDES'')
                        ') AS SAE  
                        ON CAST(SAE.ID_VANTIVE AS VARCHAR) = CAST(N.id_vgr AS VARCHAR)
                        """
        print("Executando a query...")
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return pl.DataFrame(
            data=[tuple(str(value) for value in row) for row in result],
            schema=dict(
                **{
                    k: v.get("type")
                    for k, v in self._schema_query_interfaces.items()
                }
            ),
            orient="row",
        ).rename(
            {k: v["rename"] for k, v in self._schema_query_interfaces.items()}
        )

    @transaction.atomic
    def load(self) -> None:
        self._delete()
        self._save()

    def _delete(self):
        print("Deletando os registros do banco...")
        n_deleted, __ = (
            SolarInterfaceOriginal.objects.using("power_bi")
            .filter(**self._filtro)
            .delete()
        )
        self.log["n_deleted"] = n_deleted

    def _save(self):
        print("Salvando os novos registros no banco...")
        if self.dataset.is_empty():
            return

        objs = [
            SolarInterfaceOriginal(**vals) for vals in self.dataset.to_dicts()
        ]
        bulk = SolarInterfaceOriginal.objects.using("power_bi").bulk_create(
            objs=objs, batch_size=1000
        )
        self.log["n_inserted"] = len(bulk)
        print(f"Finalizado a carga, criado {len(bulk)} registros...")


# @shared_task(
#     name="receita.load_consolidacao",
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_backoff=5,
#     retry_kwargs={"max_retries": 3},
# )
def load_interface_original_vgr_async(self, filtros: dict) -> dict:
    with LoadInterfaceOriginalVGR(**filtros) as task:
        log = task.run()
    return log
