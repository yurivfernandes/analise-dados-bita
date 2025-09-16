from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class ContractSla(models.Model):
    schedule_source = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    relative_duration_works_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    retroactive_pause = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    set_start_to = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    timezone = models.TextField(null=True, blank=True, db_collation=COLLATION)
    when_to_cancel = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    type = models.TextField(null=True, blank=True, db_collation=COLLATION)
    pause_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    duration = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_id = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cancel_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    reset_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    resume_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    reset_action = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    flow = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    stop_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    start_condition = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    schedule_source_field = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    workflow = models.TextField(null=True, blank=True, db_collation=COLLATION)
    service_commitment = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_overrides = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    adv_condition_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    collection = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain_path = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    target = models.TextField(null=True, blank=True, db_collation=COLLATION)
    schedule = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_update_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    timezone_source = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    enable_logging = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    retroactive = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    when_to_resume = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_policy = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_workflow = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_schedule = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_flow = models.TextField(null=True, blank=True, db_collation=COLLATION)

    class Meta:
        db_table = "contract_sla"
