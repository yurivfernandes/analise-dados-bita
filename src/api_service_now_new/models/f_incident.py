from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class FIncident(models.Model):
    """Tabela derivada contendo incident mesclado com informações de SLA.

    Persistimos um registro por incident (sys_id), com todas as colunas processadas na task.
    """

    # Campos básicos do incident
    sys_id = models.CharField(
        primary_key=True, max_length=255, db_collation=COLLATION
    )
    number = models.CharField(max_length=255, db_collation=COLLATION)

    # Campos de data
    data_abertura = models.DateTimeField(null=True, blank=True)
    data_fechamento = models.DateTimeField(null=True, blank=True)
    data_fim_da_indisponibilidade = models.DateTimeField(null=True, blank=True)

    # Categorias
    categoria_de_abertura = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    subcategoria_de_abertura = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    detalhe_subcategoria_de_abertura = models.CharField(
        max_length=500, null=True, blank=True, db_collation=COLLATION
    )
    categoria_da_falha = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    subcategoria_da_falha = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    detalhe_subcategoria_da_faha = models.CharField(
        max_length=500, null=True, blank=True, db_collation=COLLATION
    )

    # Campos informativos
    titulo_do_chamado = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    tipo_do_contato = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    cmdb_id = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    status = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    origem = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )

    # Campos organizacionais
    torre_de_atendimento = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    cliente = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    numero_do_contrato = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )

    # Campos de SLA
    sla_atendimento = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    sla_resolucao = models.CharField(
        max_length=255, null=True, blank=True, db_collation=COLLATION
    )
    duracao_sla_atendimento_segundos = models.FloatField(null=True, blank=True)
    duracao_sla_resolucao_segundos = models.FloatField(null=True, blank=True)

    # Campos calculados
    localidade = models.CharField(
        max_length=100, null=True, blank=True, db_collation=COLLATION
    )
    tipo_abertura = models.CharField(
        max_length=20, null=True, blank=True, db_collation=COLLATION
    )
    incidente_pai_ou_filho = models.CharField(
        max_length=10, null=True, blank=True, db_collation=COLLATION
    )
    tempo_indisponivel_segundos = models.BigIntegerField(null=True, blank=True)
    horas_trabalhadas_segundos = models.BigIntegerField(null=True, blank=True)
    prioridade = models.CharField(
        max_length=50, null=True, blank=True, db_collation=COLLATION
    )

    # Campos de controle ETL
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = "f_incident"
