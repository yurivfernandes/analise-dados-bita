from django.db import models


class ResponseTime(models.Model):
    node_id = models.CharField(max_length=100, null=True)
    date_time = models.CharField(max_length=100, null=True)
    avg_response_time = models.CharField(max_length=100, null=True)
    percent_loss = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.node_id} @ {self.date_time} -> avg {self.avg_response_time}"

    class Meta:
        db_table = "f_capacity_response_time"
        verbose_name = "Fato Response Time (Capacity)"
        verbose_name_plural = "Fato Response Times (Capacity)"
