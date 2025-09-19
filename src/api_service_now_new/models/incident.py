from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class Incident(models.Model):
    sys_id = models.TextField(db_collation=COLLATION, primary_key=True)
    number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    incident_state = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    resolved_at = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    closed_at = models.TextField(null=True, blank=True, db_collation=COLLATION)
    priority = models.TextField(null=True, blank=True, db_collation=COLLATION)
    urgency = models.TextField(null=True, blank=True, db_collation=COLLATION)
    impact = models.TextField(null=True, blank=True, db_collation=COLLATION)
    severity = models.TextField(null=True, blank=True, db_collation=COLLATION)
    category = models.TextField(null=True, blank=True, db_collation=COLLATION)
    subcategory = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_subcategory_detail = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    company = models.TextField(null=True, blank=True, db_collation=COLLATION)
    assignment_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    assigned_to = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    caller_id = models.TextField(null=True, blank=True, db_collation=COLLATION)
    resolved_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    opened_by = models.TextField(null=True, blank=True, db_collation=COLLATION)
    closed_by = models.TextField(null=True, blank=True, db_collation=COLLATION)
    short_description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    close_notes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    resolution_notes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    cmdb_ci = models.TextField(null=True, blank=True, db_collation=COLLATION)
    business_service = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_stc = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    calendar_stc = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    resolve_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    reopen_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    reopened_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    parent_incident = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    problem_id = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    change_request = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    opened_at = models.TextField(null=True, blank=True, db_collation=COLLATION)
    time_worked = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "incident"
