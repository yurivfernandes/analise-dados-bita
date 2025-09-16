from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class SysCompany(models.Model):
    sys_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255, db_collation=COLLATION)
    parent = models.CharField(
        max_length=32, null=True, blank=True, db_collation=COLLATION
    )
    customer = models.BooleanField(default=False, null=True)
    vendor = models.BooleanField(default=False, null=True)
    manufacturer = models.BooleanField(default=False, null=True)
    phone = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    fax = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    website = models.CharField(
        max_length=1024, null=True, blank=True, db_collation=COLLATION
    )
    street = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    city = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    state = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    zip = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    country = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    federal_tax_id = models.CharField(
        max_length=40, null=True, blank=True, db_collation=COLLATION
    )
    active = models.BooleanField(default=True, null=True)
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
        db_table = "sys_company"
