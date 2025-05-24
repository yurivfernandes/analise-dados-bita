from django.db import models

from .d_premissa import DPremissa


class DCriterio(models.Model):
    TIPO_CHOICES = [
        ("boolean", "Booleano"),
        ("conversao", "Conversão"),
    ]

    FIELD_SERVICENOW_CHOICES = [
        ("resolved_by", "Resolvido Por"),
        ("assignment_group", "Grupo de Atendimento"),
        ("opened_at", "Data de Abertura"),
        ("closed_at", "Data de Fechamento"),
        ("contract", "Contrato"),
        ("sla_atendimento", "SLA Atendimento"),
        ("sla_resolucao", "SLA Resolução"),
        ("company", "Cliente"),
        ("u_origem", "Torre de Atendimento"),
        ("dv_u_categoria_da_falha", "Categoria da Falha"),
        ("dv_u_sub_categoria_da_falha", "Sub Categoria da Falha"),
        ("dv_u_detalhe_sub_categoria_da_falha", "Detalhe Sub Categoria"),
        ("u_tipo_indisponibilidade", "Tipo da Indisponibilidade"),
    ]

    premissa = models.ForeignKey(
        DPremissa, on_delete=models.CASCADE, related_name="criterios"
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    ativo = models.BooleanField(default=True)
    peso = models.IntegerField()
    field_service_now = models.CharField(
        max_length=100,
        choices=FIELD_SERVICENOW_CHOICES,
        null=True,
        blank=True,
        help_text="Campo correspondente no ServiceNow",
    )

    def __str__(self):
        return f"{self.nome} - {self.premissa}"

    class Meta:
        db_table = "d_criterio"
        verbose_name = "Critério"
        verbose_name_plural = "Critérios"
