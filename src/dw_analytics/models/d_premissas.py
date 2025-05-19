from django.db import models

from .d_assignment_group import DAssignmentGroup


class DPremissas(models.Model):
    assignment = models.ForeignKey(DAssignmentGroup, on_delete=models.CASCADE)
    qtd_incidents = models.IntegerField()
    is_contrato_lancado = models.BooleanField()
    is_horas_lancadas = models.BooleanField()
    is_has_met_first_response_target = models.BooleanField()
    is_resolution_target = models.BooleanField()
    is_atualizacao_logs_correto = models.BooleanField()
    is_ticket_encerrado_corretamente = models.BooleanField()
    is_descricao_troubleshooting = models.BooleanField()
    is_cliente_notificado = models.BooleanField()
    is_category_correto = models.BooleanField()

    class Meta:
        db_table = "d_premissas"
        app_label = "dw_analytics"
