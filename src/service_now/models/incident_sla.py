from django.db import models


class IncidentSLA(models.Model):
    active = models.BooleanField(blank=True, null=True)
    business_duration = models.DateTimeField(blank=True, null=True)
    dv_business_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_pause_duration = models.DateTimeField(blank=True, null=True)
    dv_business_pause_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_percentage = models.DecimalField(
        max_digits=18, decimal_places=0, blank=True, null=True
    )
    business_time_left = models.DateTimeField(blank=True, null=True)
    dv_business_time_left = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    duration = models.DateTimeField(blank=True, null=True)
    dv_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(blank=True, null=True)
    has_breached = models.BooleanField(blank=True, null=True)
    original_breach_time = models.DateTimeField(blank=True, null=True)
    pause_duration = models.DateTimeField(blank=True, null=True)
    dv_pause_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    pause_time = models.DateTimeField(blank=True, null=True)
    percentage = models.DecimalField(
        max_digits=18, decimal_places=0, blank=True, null=True
    )
    planned_end_time = models.DateTimeField(blank=True, null=True)
    schedule = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_schedule = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sla = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_sla = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    stage = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_stage = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    start_time = models.DateTimeField(blank=True, null=True)
    sys_created_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_created_on = models.DateTimeField(blank=True, null=True)
    sys_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_mod_count = models.IntegerField(blank=True, null=True)
    sys_tags = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_updated_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_updated_on = models.DateTimeField(blank=True, null=True)
    task = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_task = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    time_left = models.DateTimeField(blank=True, null=True)
    dv_time_left = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    timezone = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_timezone = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "incident_sla"
