from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class Groups(models.Model):
    parent = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_product = models.TextField(null=True, blank=True, db_collation=COLLATION)
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_approvers = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    source = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    type = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_portfolio_coordinator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    points = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    u_product_family = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    default_assignee = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    vendors = models.TextField(null=True, blank=True, db_collation=COLLATION)
    email = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    manager = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    average_daily_fte = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_tem_roles = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_portfolio_coordinator_2 = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_idm = models.TextField(null=True, blank=True, db_collation=COLLATION)
    hourly_rate = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_roles_types = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    exclude_manager = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    include_members = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_manager = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_parent = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_u_portfolio_coordinator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_u_product_family = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_u_portfolio_coordinator_2 = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "groups"
