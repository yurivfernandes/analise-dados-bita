from django.db import models

from .d_assignment_group import DAssignmentGroup
from .d_resolved_by import DResolvedBy


class DResolvedByAssignmentGroup(models.Model):
    resolved_by = models.ForeignKey(DResolvedBy, on_delete=models.CASCADE)
    assignment_group = models.ForeignKey(
        DAssignmentGroup, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "d_resolved_by_assignment_group"
        app_label = "dw_analytics"
