from django.db import models

from .mixins import AuditMixin


class AvaliacaoTecnica(AuditMixin, models.Model):
    class Classificacao(models.TextChoices):
        BOM = "Bom", "Bom"
        OTIMO = "Ótimo", "Ótimo"
        RUIM = "Ruim", "Ruim"

    class Criterio(models.TextChoices):
        JITTER = "Jitter", "Jitter"
        LATENCIA = "Latência", "Latência"
        PERDA_PACOTE = "Perda de Pacote", "Perda de Pacote"

    class Regiao(models.TextChoices):
        CAPITAL = "Capital", "Capital"
        INTERIOR = "Interior", "Interior"

    class Tecnologia(models.TextChoices):
        FIXA = "Banda Larga Fixa", "Banda Larga Fixa"
        IP_DEDICADO = "IP Dedicado", "IP Dedicado"
        MPLS = "MPLS", "MPLS"
        MOVEL = "Banda Larga Móvel", "Banda Larga Móvel"
        SATELITE = "Banda Larga Satélite", "Banda Larga Satélite"

    classificacao = models.CharField(
        max_length=10, choices=Classificacao.choices
    )
    criterio = models.CharField(max_length=20, choices=Criterio.choices)
    faixa_min = models.FloatField()
    faixa_max = models.FloatField(null=True, blank=True)
    nota = models.PositiveSmallIntegerField()
    regiao = models.CharField(max_length=10, choices=Regiao.choices)
    tecnologia = models.CharField(max_length=30, choices=Tecnologia.choices)

    class Meta:
        db_table = "d_avaliacao_tecnica"
        verbose_name = "Avaliação Técnica"
        verbose_name_plural = "Avaliações Técnicas"
        ordering = ["tecnologia", "regiao", "criterio", "classificacao"]

    def __str__(self):
        return f"{self.tecnologia} - {self.regiao} - {self.criterio} ({self.classificacao})"
