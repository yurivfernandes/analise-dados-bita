from django.db import models


class TblSolarInterfacesVgr(models.Model):
    id = models.AutoField(
        db_column="ID", primary_key=True
    )  # Field name made lowercase.
    company_remedy = models.CharField(
        db_column="Company_Remedy",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    nome_do_cliente = models.CharField(
        db_column="Nome_do_cliente",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    razao_social = models.CharField(
        db_column="RAZAO_SOCIAL",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    grupo_corporativo = models.CharField(
        db_column="GRUPO_CORPORATIVO",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    id_vgr = models.CharField(
        db_column="ID_VGR",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    designador = models.CharField(
        db_column="DESIGNADOR",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    operadora = models.CharField(
        db_column="Operadora",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    tecnologia = models.CharField(
        db_column="Tecnologia",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    municipio = models.CharField(
        db_column="MUNICÍPIO",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    uf = models.CharField(
        db_column="UF",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    velocidade = models.CharField(
        db_column="VELOCIDADE",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    status_vantive = models.CharField(
        db_column="STATUS_VANTIVE",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    interfaceid = models.CharField(
        db_column="INTERFACEID",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    id_vantive_principal = models.CharField(
        db_column="ID_VANTIVE_PRINCIPAL",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    ip_interface = models.CharField(
        db_column="IP_Interface",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    ip_node = models.CharField(
        db_column="IP_Node",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    operadora2 = models.CharField(
        db_column="OPERADORA2",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    operadora3 = models.CharField(
        db_column="OPERADORA3",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.

    class Meta:
        db_table = "TBL_SOLAR_INTERFACES_VGR"
        app_label = "power_bi"
