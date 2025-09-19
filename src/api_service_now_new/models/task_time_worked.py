from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class TaskTimeWorked(models.Model):
    comments = models.TextField(null=True, blank=True, db_collation=COLLATION)
    work_date = models.TextField(null=True, blank=True, db_collation=COLLATION)
    time_card = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    time_worked = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    time_in_seconds = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    task = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    category = models.TextField(null=True, blank=True, db_collation=COLLATION)
    user = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_horas_billable = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_task = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_user = models.TextField(null=True, blank=True, db_collation=COLLATION)
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    etl_hash = models.TextField(null=True, blank=True, db_collation=COLLATION)
    class Meta:
        managed = False
        db_table = "task_time_worked"
