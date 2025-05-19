from django.db import models


class DResolvedBy(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    dv_resolved_by = models.CharField(
        max_length=80, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        db_table = "d_resolved_by"
        app_label = "dw_analytics"
