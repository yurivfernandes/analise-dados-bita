from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class CmdbCiNetworkLink(models.Model):
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_link_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_end_a = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_end_b = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_bandwidth = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_status = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_provider = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_type = models.TextField(null=True, blank=True, db_collation=COLLATION)
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
        db_table = "cmdb_ci_network_link"
