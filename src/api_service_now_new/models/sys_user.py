from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class SysUser(models.Model):
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    user_name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    first_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    last_name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    middle_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    email = models.TextField(null=True, blank=True, db_collation=COLLATION)
    phone = models.TextField(null=True, blank=True, db_collation=COLLATION)
    mobile_phone = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    company = models.TextField(null=True, blank=True, db_collation=COLLATION)
    department = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    manager = models.TextField(null=True, blank=True, db_collation=COLLATION)
    title = models.TextField(null=True, blank=True, db_collation=COLLATION)
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    locked_out = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    web_service_access_only = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    last_login = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    last_login_time = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    failed_attempts = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    time_zone = models.TextField(null=True, blank=True, db_collation=COLLATION)
    date_format = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    time_format = models.TextField(
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
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    etl_hash = models.TextField(null=True, blank=True, db_collation=COLLATION)

    class Meta:
        managed = False
        db_table = "sys_user"
