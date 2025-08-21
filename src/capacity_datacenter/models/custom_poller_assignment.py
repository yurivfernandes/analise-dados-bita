from django.db import models
from .mixins import AuditMixin


class CustomPollerAssignment(AuditMixin, models.Model):
    """Model para representar CustomPollerAssignment da query externa."""

    custom_poller_assignment_id = models.CharField(max_length=100, null=True)
    node_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"CPA {self.custom_poller_assignment_id} -> Node {self.node_id}"

    class Meta:
        db_table = "d_custom_poller_assignment"
        verbose_name = "Dim Custom Poller Assignment"
        verbose_name_plural = "Dim Custom Poller Assignments"
        
