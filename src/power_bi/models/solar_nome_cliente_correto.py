from django.db import models


class SolarNomeClienteCorreto(models.Model):
    id = models.AutoField(db_column="ID", primary_key=True)
    nome_solar = models.CharField(
        db_column="nome_solar",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        unique=True,
    )
    nome_correto = models.CharField(
        db_column="nome_correto",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )

    class Meta:
        db_table = "solar_nome_cliente_correto"
        app_label = "power_bi"
