# Documentação das Models do app `power_bi`

Este documento detalha cada model do app, explicando campos, tipos, relacionamentos e finalidade.

---

## `TblSolarInterfacesVgr`

```python
class TblSolarInterfacesVgr(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    company_remedy = models.CharField(db_column="Company_Remedy", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    nome_do_cliente = models.CharField(db_column="Nome_do_cliente", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    razao_social = models.CharField(db_column="RAZAO_SOCIAL", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    grupo_corporativo = models.CharField(db_column="GRUPO_CORPORATIVO", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    id_vgr = models.CharField(db_column="ID_VGR", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    designador = models.CharField(db_column="DESIGNADOR", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora = models.CharField(db_column="Operadora", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    tecnologia = models.CharField(db_column="Tecnologia", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    municipio = models.CharField(db_column="MUNICÍPIO", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    uf = models.CharField(db_column="UF", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    velocidade = models.CharField(db_column="VELOCIDADE", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    status_vantive = models.CharField(db_column="STATUS_VANTIVE", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    interfaceid = models.CharField(db_column="INTERFACEID", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    id_vantive_principal = models.CharField(db_column="ID_VANTIVE_PRINCIPAL", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    ip_interface = models.CharField(db_column="IP_Interface", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    ip_node = models.CharField(db_column="IP_Node", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora2 = models.CharField(db_column="OPERADORA2", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora3 = models.CharField(db_column="OPERADORA3", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
```
- **id**: Identificador único da interface.
- **company_remedy**: Nome da empresa Remedy.
- **nome_do_cliente**: Nome do cliente.
- **razao_social**: Razão social do cliente.
- **grupo_corporativo**: Grupo corporativo do cliente.
- **id_vgr**: Identificador VGR.
- **designador**: Designador da interface.
- **operadora**: Nome da operadora.
- **tecnologia**: Tecnologia utilizada.
- **municipio**: Município da interface.
- **uf**: Unidade federativa.
- **velocidade**: Velocidade contratada.
- **status_vantive**: Status no sistema Vantive.
- **interfaceid**: Identificador da interface.
- **id_vantive_principal**: ID principal no Vantive.
- **ip_interface**: IP da interface.
- **ip_node**: IP do nó.
- **operadora2** / **operadora3**: Operadoras adicionais.

---

## `SolarIDVGRInterfaceCorrigido`

```python
class SolarIDVGRInterfaceCorrigido(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    company_remedy = models.CharField(db_column="company_remedy", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    nome_do_cliente = models.CharField(db_column="nome_do_cliente", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    razao_social = models.CharField(db_column="razao_social", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    grupo_corporativo = models.CharField(db_column="grupo_corporativo", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    id_vgr = models.CharField(db_column="id_vgr", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    designador = models.CharField(db_column="designador", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora = models.CharField(db_column="operadora", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    tecnologia = models.CharField(db_column="tecnologia", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    municipio = models.CharField(db_column="municipio", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    uf = models.CharField(db_column="uf", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    velocidade = models.CharField(db_column="velocidade", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    status_vantive = models.CharField(db_column="status_vantive", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    interfaceid = models.CharField(db_column="interfaceid", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    id_vantive_principal = models.CharField(db_column="id_vantive_principal", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    ip_interface = models.CharField(db_column="ip_interface", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    ip_node = models.CharField(db_column="ip_node", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora2 = models.CharField(db_column="operadora2", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operadora3 = models.CharField(db_column="operadora3", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    historico_ids = models.JSONField(default=list, db_column="historico_ids")
```
- **id**: Identificador único da interface corrigida.
- **company_remedy**: Nome da empresa Remedy.
- **nome_do_cliente**: Nome do cliente.
- **razao_social**: Razão social do cliente.
- **grupo_corporativo**: Grupo corporativo do cliente.
- **id_vgr**: Identificador VGR.
- **designador**: Designador da interface.
- **operadora**: Nome da operadora.
- **tecnologia**: Tecnologia utilizada.
- **municipio**: Município da interface.
- **uf**: Unidade federativa.
- **velocidade**: Velocidade contratada.
- **status_vantive**: Status no sistema Vantive.
- **interfaceid**: Identificador da interface.
- **id_vantive_principal**: ID principal no Vantive.
- **ip_interface**: IP da interface.
- **ip_node**: IP do nó.
- **operadora2** / **operadora3**: Operadoras adicionais.
- **historico_ids**: Lista de IDs históricos relacionados à interface (campo JSON).

---

# `__init__.py` das models

O arquivo `__init__.py` importa todas as models do diretório, facilitando o import em outros módulos:

```python
from .solar_id_vgr_interface_vgr_corrigido import SolarIDVGRInterfaceCorrigido
from .tbl_solar_interfaces_vgr import TblSolarInterfacesVgr
```

## Como importar novas models

1. Crie o novo arquivo de model (ex: `nova_model.py`).
2. Importe a nova model no `__init__.py`:
    ```python
    from .nova_model import NovaModel
    ```
3. Agora, em qualquer lugar do projeto, basta importar:
    ```python
    from power_bi.models import NovaModel
    ```

> Isso mantém o código organizado e facilita a manutenção e o uso das models em views, serializers, tasks, etc.
