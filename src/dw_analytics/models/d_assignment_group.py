from django.db import models


class DAssignmentGroup(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    dv_assignment_group = models.CharField(
        max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )
    status = models.BooleanField()

    class Meta:
        db_table = "d_assignment_group"
        app_label = "dw_analytics"  # Define explicitamente o app_label
