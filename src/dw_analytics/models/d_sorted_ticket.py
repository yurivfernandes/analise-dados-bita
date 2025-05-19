from django.db import models


class DSortedTicket(models.Model):
    incident = models.CharField(
        max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )
    mes_ano = models.CharField(
        max_length=7, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        db_table = "d_sorted_ticket"
        app_label = "dw_analytics"
