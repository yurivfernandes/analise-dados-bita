from django.db import models

from .mixins import AuditMixin


class CustomPollerStatistics(AuditMixin, models.Model):
    """Model representando CustomPollerStatistics_CS da query externa."""

    node_id = models.CharField(max_length=10, null=True)
    row_id = models.CharField(max_length=100, null=True)
    date = models.DateField()
    raw_status = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def __str__(self):
        return f"CPS {self.node_id} - Row {self.row_id}"

    class Meta:
        db_table = "f_custom_poller_statistics"
        verbose_name = "Fato Custom Poller Statistics"
        verbose_name_plural = "Fato Custom Poller Statistics"
