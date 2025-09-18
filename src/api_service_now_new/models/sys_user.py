from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class SysUser(models.Model):
    sys_id = models.CharField(max_length=32, primary_key=True)
    user_name = models.CharField(max_length=40, db_collation=COLLATION)
    name = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    first_name = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    last_name = models.CharField(
        max_length=120, null=True, blank=True, db_collation=COLLATION
    )
    middle_name = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    email = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    phone = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    mobile_phone = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    company = models.CharField(
        max_length=32, null=True, blank=True, db_collation=COLLATION
    )
    department = models.CharField(
        max_length=32, null=True, blank=True, db_collation=COLLATION
    )
    location = models.CharField(
        max_length=32, null=True, blank=True, db_collation=COLLATION
    )
    manager = models.CharField(
        max_length=32, null=True, blank=True, db_collation=COLLATION
    )
    title = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    active = models.CharField(max_length=10, null=True, blank=True)
    locked_out = models.CharField(max_length=10, null=True, blank=True)
    web_service_access_only = models.CharField(
        max_length=10, null=True, blank=True
    )
    last_login = models.CharField(max_length=50, null=True, blank=True)
    last_login_time = models.CharField(max_length=50, null=True, blank=True)
    failed_attempts = models.CharField(max_length=50, null=True, blank=True)
    time_zone = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    date_format = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    time_format = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.DateTimeField(null=True, blank=True)
    sys_created_by = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.DateTimeField(null=True, blank=True)
    sys_updated_by = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    etl_created_at = models.DateTimeField(null=True, blank=True)
    etl_updated_at = models.DateTimeField(null=True, blank=True)
    etl_hash = models.CharField(
        max_length=64, null=True, blank=True, db_collation=COLLATION
    )

    class Meta:
        managed = False
        db_table = "sys_user"
