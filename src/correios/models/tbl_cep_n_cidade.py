from django.db import models


class TblCepNCidade(models.Model):
    id_cidade = models.IntegerField(primary_key=True)
    cidade = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    cidade_sem_acento = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    estado = models.CharField(
        max_length=2,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    cidade_ibge = models.CharField(
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    ddd = models.CharField(
        max_length=2,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    cidade_area = models.CharField(
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    latitude = models.CharField(
        max_length=50,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    longitude = models.CharField(
        max_length=50,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "tbl_cep_n_cidade"
