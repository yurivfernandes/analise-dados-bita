from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class SysCompany(models.Model):
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    parent = models.TextField(null=True, blank=True, db_collation=COLLATION)
    customer = models.TextField(null=True, blank=True, db_collation=COLLATION)
    vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    manufacturer = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    phone = models.TextField(null=True, blank=True, db_collation=COLLATION)
    fax = models.TextField(null=True, blank=True, db_collation=COLLATION)
    website = models.TextField(null=True, blank=True, db_collation=COLLATION)
    street = models.TextField(null=True, blank=True, db_collation=COLLATION)
    city = models.TextField(null=True, blank=True, db_collation=COLLATION)
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    zip = models.TextField(null=True, blank=True, db_collation=COLLATION)
    country = models.TextField(null=True, blank=True, db_collation=COLLATION)
    federal_tax_id = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
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
        db_table = "sys_company"
