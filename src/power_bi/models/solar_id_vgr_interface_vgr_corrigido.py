from django.db import models


class SolarIDVGRInterfaceCorrigido(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    company_remedy = models.CharField(
        db_column="company_remedy",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    nome_do_cliente = models.CharField(
        db_column="nome_do_cliente",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    razao_social = models.CharField(
        db_column="razao_social",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    grupo_corporativo = models.CharField(
        db_column="grupo_corporativo",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    id_vgr = models.CharField(
        db_column="id_vgr",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    designador = models.CharField(
        db_column="designador",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    operadora = models.CharField(
        db_column="operadora",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    tecnologia = models.CharField(
        db_column="tecnologia",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    municipio = models.CharField(
        db_column="municipio",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    uf = models.CharField(
        db_column="uf",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    velocidade = models.CharField(
        db_column="velocidade",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    status_vantive = models.CharField(
        db_column="status_vantive",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    interfaceid = models.CharField(
        db_column="interfaceid",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    id_vantive_principal = models.CharField(
        db_column="id_vantive_principal",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    ip_interface = models.CharField(
        db_column="ip_interface",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    ip_node = models.CharField(
        db_column="ip_node",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    operadora2 = models.CharField(
        db_column="operadora2",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    operadora3 = models.CharField(
        db_column="operadora3",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    historico_ids = models.JSONField(default=list, db_column="historico_ids")

    class Meta:
        db_table = "solar_id_vgr_interface_corrigido"
        app_label = "power_bi"
