from django.db import models


class Node(models.Model):
    nome_do_cliente = models.CharField(max_length=255, null=True)
    node_id = models.CharField(max_length=10, null=True)
    id_vgr = models.CharField(max_length=7, null=True)
    caption = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    automatizacao = models.CharField(max_length=20, null=True)
    redundancia = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.nome_do_cliente} - {self.node_id}"

    class Meta:
        db_table = "d_node"
        verbose_name = "Dim Node (Capacity)"
        verbose_name_plural = "Dim Nodes (Capacity)"
