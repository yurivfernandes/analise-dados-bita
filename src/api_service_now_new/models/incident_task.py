from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class IncidentTask(models.Model):
    parent = models.TextField(null=True, blank=True, db_collation=COLLATION)
    watch_list = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_tempo_indisponivel = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    upon_reject = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    approval_history = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    skills = models.TextField(null=True, blank=True, db_collation=COLLATION)
    number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_contact_attempt = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_detalhe_subcategoria_de_produto_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_codigo_reserva = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_cliente_detrator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_designa_o_lp = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    knowledge = models.TextField(null=True, blank=True, db_collation=COLLATION)
    order = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_rma = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cmdb_ci = models.TextField(null=True, blank=True, db_collation=COLLATION)
    delivery_plan = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_carimbo_certificacao_remota = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract = models.TextField(null=True, blank=True, db_collation=COLLATION)
    impact = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_ordem_de_venda = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    work_notes_list = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_solicitacao_envio_equipamento_defeituoso = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    priority = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_domain_path = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    group_list = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_nome_fabricante = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_motivo = models.TextField(null=True, blank=True, db_collation=COLLATION)
    approval_set = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_in_cio = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_opened_month = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    needs_attention = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    universal_request = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    short_description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_entrega_cliente = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    correlation_display = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    delivery_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    work_start = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_complaint = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    additional_assignee_list = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_current_activity = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_fabricante = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_part_number_retirado = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_produto = models.TextField(null=True, blank=True, db_collation=COLLATION)
    service_offering = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    closed_by = models.TextField(null=True, blank=True, db_collation=COLLATION)
    follow_up = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_operadora_integrador = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_case_encerrado = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_follow_up_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    reassignment_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_cmdb_ci = models.TextField(null=True, blank=True, db_collation=COLLATION)
    assigned_to = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_acionamento = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sla_due = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_ticket_fabricante = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_visita_tecnica = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    agile_story = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_outro_fabricante = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    escalation = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    upon_approval = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_inicio_sprint = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    correlation_id = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_nome_produto = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_protocolo = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_sub_categoria_de_causa_raiz = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    made_sla = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_data_retirada = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_serial_number_retirado = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_codigo_de_rastreio = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    task_effective_number = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_de_entrega = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    opened_by = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_assigned_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    user_input = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_task_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_instalacao = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_carimbo_prazo_reparo = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    route_reason = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_serial_number = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_validacao_configuracao = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_categoria_de_prooduto_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    closed_at = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_data_validacao_estoque = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_saida_site = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sn_ind_tsm_core_stage_created = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_service = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    time_worked = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_tipo_da_tarefa = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    expected_start = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_fabricante_retirado = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_part_number = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_tempo_expurgo = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    opened_at = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_cmdb_ci_secundario = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_teste_funcional = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    work_end = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_outros = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_atualizacao_cmdb = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_detalhe_sub_categoria_de_causa_raiz = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    work_notes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_follow_up_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_tipo_acionamento = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    assignment_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_categoria_de_causa_raiz = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_envio_nf_ups = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_total_task_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    calendar_duration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_equipamento_entregue_ups = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_descricao_equipamento_defeituoso = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    close_notes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_categoria_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_complaint_sub = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_detalhe_subcategoria_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    contact_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_efetividade = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    urgency = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_certificacao_origem = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_de_envio = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    company = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_last_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_subcategoria_de_produto_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    activity_due = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_nota_fiscal = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    action_status = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_duration_of_negotiations = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_current_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_outros_servicos = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_data_fim = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    comments = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_task_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    approval = models.TextField(null=True, blank=True, db_collation=COLLATION)
    due_date = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_entrada_site = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_close_code = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_subcategoria_iot_task = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    incident = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_parent = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_closed_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_assigned_to = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_opened_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_assignment_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_company = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_incident = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    etl_created_at = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    etl_updated_at = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    class Meta:
        managed = False
        db_table = "incident_task"
