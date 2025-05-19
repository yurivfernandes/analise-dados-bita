from django.db import models


class FSaeLocalidades(models.Model):
    id_vantive = models.IntegerField(
        db_column="ID_VANTIVE", blank=True, null=True
    )  # Field name made lowercase.
    uf = models.CharField(
        db_column="UF",
        max_length=20,
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
    data_rfb = models.DateField(
        db_column="DATA_RFB", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "f_sae_localidades"
        app_label = "dw_analytics"
