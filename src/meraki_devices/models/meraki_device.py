from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    serial = models.CharField(max_length=50)
    mac = models.CharField(max_length=17, null=True)
    networkId = models.CharField(max_length=50, null=True)
    productType = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    notes = models.TextField(null=True)
    wan1Ip = models.GenericIPAddressField(null=True)
    wan2Ip = models.GenericIPAddressField(null=True)
    configurationUpdatedAt = models.DateTimeField(null=True)
    firmware = models.CharField(max_length=50, null=True)
    url = models.URLField(null=True)
    tags = models.JSONField(null=True)
    details = models.JSONField(null=True)
    organization_id = models.CharField(max_length=50)
    lanIp = models.GenericIPAddressField(null=True)
    
    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        db_table = "meraki_device"
        verbose_name = "Dispositivo Meraki"
        verbose_name_plural = "Dispositivos Meraki"
