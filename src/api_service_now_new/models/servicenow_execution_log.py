import uuid

from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class ServiceNowExecutionLog(models.Model):
    execution_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    execution_type = models.CharField(max_length=20, db_collation=COLLATION)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(max_length=20, db_collation=COLLATION)
    json_storage_enabled = models.BooleanField(default=False, null=True)
    total_api_requests = models.IntegerField(default=0, null=True)
    failed_api_requests = models.IntegerField(default=0, null=True)
    total_api_time_seconds = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    api_success_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True
    )
    total_db_transactions = models.IntegerField(default=0, null=True)
    total_records_processed = models.IntegerField(default=0, null=True)
    db_time_seconds = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    json_size_kb = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    compressed_size_kb = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    compression_ratio = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    tables_processed = models.CharField(
        max_length=500, null=True, blank=True, db_collation=COLLATION
    )
    error_message = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    records_by_table = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    hostname = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    username = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "servicenow_execution_log"
