# Documentação das Models do app `dw_analytics`

Este documento detalha cada model do app, explicando campos, tipos, relacionamentos e finalidade.

---

## `DAssignmentGroup`

```python
class DAssignmentGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    dv_assignment_group = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    status = models.BooleanField()
```
- **id**: Identificador único do grupo de atendimento (string).
- **dv_assignment_group**: Nome do grupo.
- **status**: Indica se o grupo está ativo.

---

## `DCompany`

```python
class DCompany(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    dv_company = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    u_cnpj = models.CharField(max_length=14, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
```
- **id**: Identificador único da empresa.
- **dv_company**: Nome da empresa.
- **u_cnpj**: CNPJ da empresa.

---

## `DContract`

```python
class DContract(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    dv_contract = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
```
- **id**: Identificador do contrato.
- **dv_contract**: Nome ou código do contrato.

---

## `DOperacao`

```python
class DOperacao(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    dv_company = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    operacao = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
```
- **id**: Identificador da operação.
- **dv_company**: Empresa relacionada.
- **operacao**: Nome da operação.

---

## `DPremissas`

```python
class DPremissas(models.Model):
    assignment = models.ForeignKey(DAssignmentGroup, on_delete=models.CASCADE)
    qtd_incidents = models.IntegerField()
    is_contrato_lancado = models.BooleanField()
    is_horas_lancadas = models.BooleanField()
    is_has_met_first_response_target = models.BooleanField()
    is_resolution_target = models.BooleanField()
    is_atualizacao_logs_correto = models.BooleanField()
    is_ticket_encerrado_corretamente = models.BooleanField()
    is_descricao_troubleshooting = models.BooleanField()
    is_cliente_notificado = models.BooleanField()
    is_category_correto = models.BooleanField()
```
- **assignment**: FK para grupo de atendimento.
- **qtd_incidents**: Quantidade de incidentes.
- **is_*:** Diversos campos booleanos para controle de premissas de qualidade.

---

## `DResolvedBy`

```python
class DResolvedBy(models.Model):
    id = models.CharField(primary_key=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    dv_resolved_by = models.CharField(max_length=80, db_collation="SQL_Latin1_General_CP1_CI_AS")
```
- **id**: Identificador do resolvedor.
- **dv_resolved_by**: Nome do resolvedor.

---

## `DResolvedByAssignmentGroup`

```python
class DResolvedByAssignmentGroup(models.Model):
    assignment_group = models.ForeignKey(DAssignmentGroup, on_delete=models.CASCADE)
    resolved_by = models.ForeignKey(DResolvedBy, on_delete=models.CASCADE)
```
- **assignment_group**: FK para grupo de atendimento.
- **resolved_by**: FK para resolvedor.

---

## `DSortedTicket`

```python
class DSortedTicket(models.Model):
    incident = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    mes_ano = models.CharField(max_length=7, db_collation="SQL_Latin1_General_CP1_CI_AS")
```
- **incident**: Identificador do incidente.
- **mes_ano**: Mês e ano do ticket.

---

## `FIncident`

```python
class FIncident(models.Model):
    number = models.CharField(unique=True, max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS")
    resolved_by = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    assignment_group = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    opened_at = models.DateTimeField()
    closed_at = models.DateTimeField(blank=True, null=True)
    contract = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    sla_atendimento = models.BooleanField(blank=True, null=True)
    sla_resolucao = models.BooleanField(blank=True, null=True)
    company = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_origem = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_u_categoria_da_falha = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_u_sub_categoria_da_falha = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_u_detalhe_sub_categoria_da_falha = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_state = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_id_vgr = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_id_vantive = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_category = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_subcategory = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_u_detail_subcategory = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_tipo_indisponibilidade = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    sys_id = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    resolved_at = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    scr_vendor_ticket = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_tipo_de_procedencia = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_sla_resolved = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_sla_first = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
```
- Campos principais de um incidente, incluindo datas, grupos, status, SLA, etc.

---

## `FIncidentsBita`

```python
class FIncidentsBita(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    assignment_group = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    resolved_at = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_origem = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    opened_at = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    opened_by = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    assigned_to = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    resolved_by = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    description = models.TextField(db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    short_description = models.TextField(db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    dv_state = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    close_notes = models.CharField(max_length=1000, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
```
- Campos principais de incidentes BITA, incluindo descrições, datas, responsáveis, prioridade, etc.

---

## `FIncidentTask`

```python
class FIncidentTask(models.Model):
    incident = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_operadora_integrador = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_outros = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_designa_o_lp = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_protocolo = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_data_in_cio = models.DateTimeField(blank=True, null=True)
    u_data_fim = models.DateTimeField(blank=True, null=True)
    u_tipo_acionamento = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
    u_produto = models.CharField(max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True)
```
- Campos de tarefas relacionadas a incidentes.

---

## `FPlantaVgr`

```python
class FPlantaVgr(models.Model):
    id_vantive = models.IntegerField(db_column="ID_VANTIVE", blank=True, null=True)
    raiz_cod_cli = models.BigIntegerField(db_column="RAIZ_COD_CLI", blank=True, null=True)
    cod_grupo = models.DecimalField(db_column="COD_GRUPO", max_digits=18, decimal_places=0, blank=True, null=True)
    cliente = models.CharField(db_column="CLIENTE", max_length=300, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    grupo_economico = models.CharField(db_column="GRUPO_ECONOMICO", max_length=350, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    cnpj = models.CharField(db_column="CNPJ", max_length=30, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    status_vantive = models.CharField(db_column="STATUS_VANTIVE", max_length=250, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    servico = models.CharField(db_column="SERVICO", max_length=100, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    endereco_completo = models.TextField(db_column="ENDERECO_COMPLETO", db_collation="Latin1_General_CI_AS", blank=True, null=True)
    cidade = models.CharField(db_column="CIDADE", max_length=100, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    uf = models.CharField(db_column="UF", max_length=20, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    cep = models.CharField(db_column="CEP", max_length=10, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    regional = models.CharField(db_column="REGIONAL", max_length=100, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    data_contrato = models.DateTimeField(db_column="DATA_CONTRATO", blank=True, null=True)
    data_entrada = models.DateField(db_column="DATA_ENTRADA", blank=True, null=True)
    data_rfs = models.DateField(db_column="DATA_RFS", blank=True, null=True)
    data_rfb = models.DateField(db_column="DATA_RFB", blank=True, null=True)
    data_rfb_nao_faturavel = models.DateTimeField(db_column="DATA_RFB_NAO_FATURAVEL", blank=True, null=True)
    data_cancelamento = models.DateTimeField(db_column="DATA_CANCELAMENTO", blank=True, null=True)
    isis_cancelamento_motivo = models.CharField(db_column="ISIS_CANCELAMENTO_MOTIVO", max_length=100, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    justif_rfb = models.CharField(db_column="JUSTIF_RFB", max_length=50, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    isis_motivo_pendencia = models.CharField(db_column="ISIS_MOTIVO_PENDENCIA", max_length=300, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    combo = models.IntegerField(db_column="COMBO", blank=True, null=True)
    caixa_unica = models.IntegerField(db_column="CAIXA_UNICA", blank=True, null=True)
    revenda_vgr = models.IntegerField(db_column="REVENDA_VGR", blank=True, null=True)
    modelo_atributos = models.CharField(db_column="MODELO_ATRIBUTOS", max_length=250, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    projeto_especial = models.CharField(db_column="PROJETO_ESPECIAL", max_length=20, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    delta_rec_liq = models.FloatField(db_column="DELTA_REC_LIQ", blank=True, null=True)
```
- Campos detalhados de planta VGR, incluindo cliente, grupo, datas, valores, etc.

---

## `FSaeLocalidades`

```python
class FSaeLocalidades(models.Model):
    id_vantive = models.IntegerField(db_column="ID_VANTIVE", blank=True, null=True)
    uf = models.CharField(db_column="UF", max_length=20, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    cidade = models.CharField(db_column="CIDADE", max_length=100, db_collation="Latin1_General_CI_AS", blank=True, null=True)
    data_rfb = models.DateField(db_column="DATA_RFB", blank=True, null=True)
```
- Campos de localidades SAE, como cidade, UF, data, etc.

---

# `__init__.py` das models

O arquivo `__init__.py` importa todas as models do diretório, facilitando o import em outros módulos:

```python
from .d_assignment_group import DAssignmentGroup
from .d_company import DCompany
from .d_contract import DContract
from .d_operacao import DOperacao
from .d_premissas import DPremissas
from .d_resolved_by import DResolvedBy
from .d_resolved_by_assignment_group import DResolvedByAssignmentGroup
from .d_sorted_ticket import DSortedTicket
from .f_incident import FIncident
from .f_incident_bita import FIncidentsBita
from .f_incident_task import FIncidentTask
from .f_planta_vgr import FPlantaVgr
from .f_sae_localidades import FSaeLocalidades
```

## Como importar novas models

1. Crie o novo arquivo de model (ex: `nova_model.py`).
2. Importe a nova model no `__init__.py`:
    ```python
    from .nova_model import NovaModel
    ```
3. Agora, em qualquer lugar do projeto, basta importar:
    ```python
    from dw_analytics.models import NovaModel
    ```

> Isso mantém o código organizado e facilita a manutenção e o uso das models em views, serializers, tasks, etc.
