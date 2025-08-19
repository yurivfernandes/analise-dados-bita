from django.db import models


class TblCepNBairro(models.Model):
    id_bairro = models.IntegerField(primary_key=True)
    bairro = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    bairro_sem_acento = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    cidade_id = models.IntegerField(blank=True, null=True)
    estado = models.CharField(
        max_length=2,
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
        db_table = "tbl_cep_n_bairro"
