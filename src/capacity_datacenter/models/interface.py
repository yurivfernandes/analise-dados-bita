from django.db import models

from .mixins import AuditMixin


class Interface(AuditMixin, models.Model):
    node_id = models.CharField(max_length=100, null=True)
    interface_id = models.CharField(max_length=100, null=True)
    interface_name = models.CharField(max_length=255, null=True)
    caption = models.CharField(max_length=255, null=True)
    id_vgr = models.CharField(max_length=100, null=True)
    servico = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.node_id} - {self.interface_id} ({self.caption})"

    class Meta:
        db_table = "d_interface"
        verbose_name = "Dim Interface (Capacity)"
        verbose_name_plural = "Dim Interfaces (Capacity)"
