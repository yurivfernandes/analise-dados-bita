from django.db import models


class FIncidentsBita(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(
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
    resolved_at = models.CharField(
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
    opened_at = models.CharField(
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
    resolved_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )
    short_description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )
    dv_state = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    close_notes = models.CharField(
        max_length=1000,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    priority = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "f_incidents_bita"
        app_label = "dw_analytics"
