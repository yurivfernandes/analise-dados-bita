from django.db import models


class CustomPollerStatistics(models.Model):
    """Model representando CustomPollerStatistics_CS da query externa."""

    custom_poller_assignment_id = models.CharField(max_length=100, null=True)
    node_id = models.CharField(max_length=100, null=True)
    row_id = models.CharField(max_length=100, null=True)
    date_time = models.CharField(max_length=100, null=True)
    raw_status = models.CharField(max_length=255, null=True)
    weight = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"CPS {self.custom_poller_assignment_id} - Row {self.row_id}"

    class Meta:
        db_table = "f_custom_poller_statistics"
        verbose_name = "Fato Custom Poller Statistics"
        verbose_name_plural = "Fato Custom Poller Statistics"
