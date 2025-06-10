from django.db import models


class SolarInterfaceOriginal(models.Model):
    nome_cliente = models.CharField(max_length=255)
    company_remedy = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    grupo_corporativo = models.CharField(max_length=255)
    id_vgr = models.CharField(max_length=255)
    designador = models.CharField(max_length=255)
    operadora = models.CharField(max_length=255)
    nome_operadora = models.CharField(max_length=255)
    nome_operadora_atual = models.CharField(max_length=255)
    tecnologia = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)
    velocidade = models.CharField(max_length=255)
    banda_contratada_entrada = models.CharField(max_length=255)
    status_vantive = models.CharField(max_length=255)
    interface_id = models.CharField(max_length=255)
    ip_interface = models.CharField(max_length=255)
    ip_node = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    interface_name = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    nome_interface = models.CharField(max_length=255)

    class Meta:
        db_table = "solar_interface_original"
        app_label = "power_bi"
