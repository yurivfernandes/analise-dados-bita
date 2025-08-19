from django.db import models

from .tbl_cep_n_bairro import TblCepNBairro
from .tbl_cep_n_cidade import TblCepNCidade
from .tbl_cep_n_distrito import TblCepNDistrito


class TblCepNLogradouro(models.Model):
    cep = models.CharField(
        max_length=8,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    tipo = models.CharField(
        max_length=50,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    nome_logradouro = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    logradouro = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    bairro = models.ForeignKey(
        TblCepNBairro, models.DO_NOTHING, blank=True, null=True
    )
    distrito = models.ForeignKey(
        TblCepNDistrito, models.DO_NOTHING, blank=True, null=True
    )
    cidade = models.ForeignKey(
        TblCepNCidade, models.DO_NOTHING, blank=True, null=True
    )
    estado = models.CharField(
        max_length=2,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    tipo_sem_acento = models.CharField(
        max_length=50,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    nome_logradouro_sem_acento = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    logradouro_sem_acento = models.CharField(
        max_length=100,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    latitude = models.CharField(
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    longitude = models.CharField(
        max_length=20,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )
    cep_ativo = models.CharField(
        max_length=1,
        db_collation="Latin1_General_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "tbl_cep_n_logradouro"
