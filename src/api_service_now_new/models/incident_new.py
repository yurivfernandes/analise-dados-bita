from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class IncidentNew(models.Model):
    number = models.CharField(
        unique=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    resolved_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    assignment_group = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    opened_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    contract = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    company = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_origem = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_sub_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detalhe_sub_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_vgr = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_vantive = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    category = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    subcategory = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detail_subcategory = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_indisponibilidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        primary_key=True,
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    scr_vendor_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_de_procedencia = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_normalizacao_servico = models.DateTimeField(
        null=True,
        blank=True,
    )
    u_vendor_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_justificativa_isolamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tempo_indisponivel = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    parent_incident = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    short_description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )
    location = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )
    contact_type = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    urgency = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    closed_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    opened_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    assigned_to = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_fim_indisponibilidade = models.DateTimeField(
        null=True,
        blank=True,
    )
    time_worked = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    priority = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    cmdb_ci = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "incident_new"
