from django.db import models


class DeviceInventario(models.Model):
    name = models.CharField(max_length=100)
    serial = models.CharField(max_length=50)
    networkId = models.CharField(max_length=50, null=True)
    productType = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    wan1Ip = models.GenericIPAddressField(null=True)
    wan2Ip = models.GenericIPAddressField(null=True)
    firmware = models.CharField(max_length=50, null=True)
    organization_id = models.CharField(max_length=50)
    lanIp = models.GenericIPAddressField(null=True)
    sigla = models.CharField(max_length=50, null=True)
    status_migrado = models.BooleanField()
    note_1 = models.CharField(max_length=1000, null=True)
    note_2 = models.CharField(max_length=1000, null=True)
    note_3 = models.CharField(max_length=1000, null=True)
    note_4 = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        db_table = "meraki_device_inventario"
        verbose_name = "Inventário de Dispositivo Meraki"
        verbose_name_plural = "Inventário de Dispositivos Meraki"
