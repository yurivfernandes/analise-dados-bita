from django.db import models


class DCompany(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    dv_company = models.CharField(
        max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )
    u_cnpj = models.CharField(
        max_length=14,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "d_company"
        app_label = "dw_analytics" 
