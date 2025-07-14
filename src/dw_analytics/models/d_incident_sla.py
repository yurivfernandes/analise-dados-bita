from django.db import models


class DIncidentSla(models.Model):
    id = models.IntegerField(primary_key=True)
    ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    nome = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=6,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "d_incident_sla"
