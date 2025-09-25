from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class Incident(models.Model):
    parent = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_parent = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    caused_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tempo_indisponivel = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_updated_on = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_vantive = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_nome_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_cidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_created_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_severidade_do_chamado = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    impact = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_de_negocio = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_rpt_tempo_de_abertura_encerramento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_cnpj = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    correlation_display = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detalhe_solucoes = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detalhe_sub_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    scr_vendor = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    service_offering = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    parent_incident = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_parent_incident = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    reopened_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_torre_de_atendimento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_ip_origin = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_anexo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_numero_do_contrato_voz = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_servico_normalizado = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_rede = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_line = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_telefone_do_responsavel = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    scr_vendor_closed_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tempo_total_da_tratativa = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_client = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    correlation_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    timeline = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_comentarios_adicionais = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_service_type = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_contato_nome = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_contato_email = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_signal_rule_description = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_origem = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_endereco_do_ponto = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_rpt_tempo_de_processamento_da_automacao_ate_abertura_do_ticket = (
        models.CharField(
            max_length=255,
            db_collation="SQL_Latin1_General_CP1_CI_AS",
            blank=True,
            null=True,
        )
    )
    hold_reason = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_classificacao_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_created_on = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_nome_do_ponto = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_serial_number = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    calendar_stc = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_company_name = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_de_agendamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_incidente = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    closed_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_impact = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_uf = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    time_worked = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_task_acionamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_integration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tempo_expurgo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_sigla_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    work_end = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_sigla_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_de_acionamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    subcategory = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    work_notes = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_sla_tratativa = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_product_subcategory_detail = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    close_code = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    assignment_group = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_assignment_group = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categoria_de_causa_raiz = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_normalizacao_servico = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_do_ponto = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_user_agent = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_endereco_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_stc = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_indisponibilidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )  # This field type is a guess.
    origin_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_justificativa = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        primary_key=True,
    )
    u_id_do_solicitante = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_opening_reason = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_fim_indisponibilidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_fornecedor_cliente = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    urgency = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    company = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_company = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    severity = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    approval = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_number_sigitm = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tempo_total_de_espera = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_alert_name = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_e_hora_da_visita_tecnica = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_produto_n1 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_tags = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_produto_n2 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_numero_do_contrato_dados = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_produto_n3 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_da_unidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categorizacao_n3 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_product_vivo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categorizacao_n1 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    scr_vendor_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categorizacao_n2 = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_previsao_de_atendimento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_location = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_de_procedencia = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_impact_do_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_protocolo_fornecedor = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    upon_reject = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    origin_table = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    approval_history = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_b2b_downtime = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_prevista_atendimento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    number = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    proposed_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_contatos_adicionais = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_ip_destination = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_serial_do_equipamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_motivo_sintoma = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_cep = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_unidade_caixa = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_chamado_tratado_por_analista = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_bradesco_ci = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    cmdb_ci = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_cmdb_ci = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    contract = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_grupo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    work_notes_list = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    priority = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_domain_path = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_type_ritm_or_incident = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_justificativa_altera_o_sintoma = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_do_estabelecimento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detalhes_adicionais = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_opened_month = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_product_category = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_descri_o_do_problema = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    short_description = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )
    u_detail_subcategory = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    work_start = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_complaint = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_endereco_da_localidade = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_justificativa_isolamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    notify = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_class_name = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_comment_inserted = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    closed_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_reincidencia = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_expected_service_time = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_rpt_tempo_detecao_hora = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_cmdb_ci = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_designador = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    assigned_to = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_assigned_to = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_identificacao_do_hardware = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sla_due = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    upon_approval = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_inicio_sprint = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    scr_vendor_opened_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_sub_categoria_de_causa_raiz = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_designador_do_circuito = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_sub_categoria_da_falha = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_resolution_time = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_ticket_sigtm_number = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    child_incidents = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    task_effective_number = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    resolved_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_resolved_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_customer_pending_time = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_updated_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    opened_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_opened_by = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sys_domain = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_sys_domain = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    proposed_on = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_identificacao_do_ponto = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_ticket_remedy_number = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_observacao_da_perda_do_sla = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    scr_vendor_resolved_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    business_service = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_hostname = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    expected_start = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    opened_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    caller_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    reopened_time = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    resolved_at = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_lp = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_rpt_tempo_de_deteccao_do_inc_ate_a_abertura_do_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_detalhe_sub_categoria_de_causa_raiz = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_tipo_de_servico = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    cause = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_vendor_ticket = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    calendar_duration = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_data_e_hora_do_agendamento = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    close_notes = models.TextField(
        db_collation="SQL_Latin1_General_CP1_CI_AS", blank=True, null=True
    )  # This field type is a guess.
    u_product_subcategory = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    contact_type = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_service_time = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    incident_state = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    problem_id = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_procedencia = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    comments = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_link_type = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    due_date = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_nome_do_respons_vel_pela_abertura_do_chamado = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_contato_telefone = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_identification = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_id_vgr = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    u_case_ticket_vivo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dv_u_case_ticket_vivo = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    category = models.CharField(
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    etl_created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    etl_updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "incident"
