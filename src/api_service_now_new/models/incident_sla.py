from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class IncidentSla(models.Model):
    pause_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    pause_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    timezone = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_time_left = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    duration = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    time_left = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    percentage = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    original_breach_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_percentage = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    end_time = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    business_pause_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sla = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_rpt_tempo_decorrido = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    schedule = models.TextField(null=True, blank=True, db_collation=COLLATION)
    start_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    task = models.TextField(null=True, blank=True, db_collation=COLLATION)
    stage = models.TextField(null=True, blank=True, db_collation=COLLATION)
    planned_end_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    has_breached = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_sla = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_schedule = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_task = models.TextField(null=True, blank=True, db_collation=COLLATION)
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "incident_sla"
