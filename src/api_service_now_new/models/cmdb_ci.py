from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class CmdbCi(models.Model):
    sys_id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    sys_class_name = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    cmdb_ci = models.TextField(null=True, blank=True, db_collation=COLLATION)
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
        db_table = "cmdb_ci"
