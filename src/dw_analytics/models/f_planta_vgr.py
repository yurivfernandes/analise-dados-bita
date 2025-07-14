from django.db import models


class FPlantaVgr(models.Model):
    id_vantive = models.IntegerField(
        db_column="ID_VANTIVE", blank=True, null=True
    )  # Field name made lowercase.
    raiz_cod_cli = models.BigIntegerField(
        db_column="RAIZ_COD_CLI", blank=True, null=True
    )  # Field name made lowercase.
    cod_grupo = models.DecimalField(
        db_column="COD_GRUPO",
        max_digits=18,
        decimal_places=0,
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cliente = models.CharField(
        db_column="CLIENTE",
        max_length=300,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    grupo_economico = models.CharField(
        db_column="GRUPO_ECONOMICO",
        max_length=350,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cnpj = models.CharField(
        db_column="CNPJ",
        max_length=30,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    status_vantive = models.CharField(
        db_column="STATUS_VANTIVE",
        max_length=250,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    servico = models.CharField(
        db_column="SERVICO",
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    endereco_completo = models.TextField(
        db_column="ENDERECO_COMPLETO",
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cidade = models.CharField(
        db_column="CIDADE",
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    uf = models.CharField(
        db_column="UF",
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    cep = models.CharField(
        db_column="CEP",
        max_length=10,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    regional = models.CharField(
        db_column="REGIONAL",
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    data_contrato = models.DateTimeField(
        db_column="DATA_CONTRATO", blank=True, null=True
    )  # Field name made lowercase.
    data_entrada = models.DateField(
        db_column="DATA_ENTRADA", blank=True, null=True
    )  # Field name made lowercase.
    data_rfs = models.DateField(
        db_column="DATA_RFS", blank=True, null=True
    )  # Field name made lowercase.
    data_rfb = models.DateField(
        db_column="DATA_RFB", blank=True, null=True
    )  # Field name made lowercase.
    data_rfb_nao_faturavel = models.DateTimeField(
        db_column="DATA_RFB_NAO_FATURAVEL", blank=True, null=True
    )  # Field name made lowercase.
    data_cancelamento = models.DateTimeField(
        db_column="DATA_CANCELAMENTO", blank=True, null=True
    )  # Field name made lowercase.
    isis_cancelamento_motivo = models.CharField(
        db_column="ISIS_CANCELAMENTO_MOTIVO",
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    justif_rfb = models.CharField(
        db_column="JUSTIF_RFB",
        max_length=50,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    isis_motivo_pendencia = models.CharField(
        db_column="ISIS_MOTIVO_PENDENCIA",
        max_length=300,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    combo = models.IntegerField(
        db_column="COMBO", blank=True, null=True
    )  # Field name made lowercase.
    caixa_unica = models.IntegerField(
        db_column="CAIXA_UNICA", blank=True, null=True
    )  # Field name made lowercase.
    revenda_vgr = models.IntegerField(
        db_column="REVENDA_VGR", blank=True, null=True
    )  # Field name made lowercase.
    modelo_atributos = models.CharField(
        db_column="MODELO_ATRIBUTOS",
        max_length=250,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    projeto_especial = models.CharField(
        db_column="PROJETO_ESPECIAL",
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    delta_rec_liq = models.FloatField(
        db_column="DELTA_REC_LIQ", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "f_planta_vgr"
