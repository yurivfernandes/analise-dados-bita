from django.db import models
from .mixins import AuditMixin


class InterfaceTraffic(AuditMixin, models.Model):
    node_id = models.CharField(max_length=100, null=True)
    date = models.DateField()
    in_average_bps = models.FloatField(null=True)
    out_average_bps = models.FloatField(null=True)

    def __str__(self):
        return f"{self.node_id} @ {self.date} -> in {self.in_average_bps} out {self.out_average_bps}"

    class Meta:
        db_table = "f_interface_traffic"
        verbose_name = "Fato Interface Traffic (Capacity)"
        verbose_name_plural = "Fato Interface Traffics (Capacity)"