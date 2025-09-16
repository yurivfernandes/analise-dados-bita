CREATE TABLE NID_QA.dbo.contract_sla (
	schedule_source nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	relative_duration_works_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	retroactive_pause nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	set_start_to nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	timezone nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	when_to_cancel nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[type] nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	pause_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_class_name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	cancel_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	vendor nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_domain nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	reset_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resume_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	reset_action nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	flow nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	stop_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	start_condition nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	schedule_source_field nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	workflow nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	service_commitment nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_mod_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_overrides nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	adv_condition_type nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	collection nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_domain_path nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_tags nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	target nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	schedule nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_update_name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	timezone_source nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	enable_logging nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	retroactive nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	when_to_resume nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_policy nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_sys_domain nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_workflow nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_schedule nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_flow nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- NID_QA.dbo.groups definition

-- Drop table

-- DROP TABLE NID_QA.dbo.groups;

CREATE TABLE NID_QA.dbo.groups (
	parent nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_product nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_approvers nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[source] nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[type] nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_portfolio_coordinator nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	points nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_product_family nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	default_assignee nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	vendors nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	email nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	manager nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_mod_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	average_daily_fte nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_tags nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_tem_roles nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_portfolio_coordinator_2 nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	cost_center nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_idm nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	hourly_rate nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_roles_types nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	exclude_manager nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	include_members nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_manager nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_parent nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_cost_center nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_u_portfolio_coordinator nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_u_product_family nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_u_portfolio_coordinator_2 nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- NID_QA.dbo.incident definition

-- Drop table

-- DROP TABLE NID_QA.dbo.incident;

CREATE TABLE NID_QA.dbo.incident (
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	number nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	state nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	incident_state nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resolved_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	closed_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	priority nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	urgency nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	impact nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	severity nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	category nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	subcategory nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_subcategory_detail nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	company nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	assignment_group nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	assigned_to nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	caller_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resolved_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	opened_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	closed_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	short_description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	close_notes nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resolution_notes nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	location nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	cmdb_ci nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_service nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_stc nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	calendar_stc nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	resolve_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	reopen_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	reopened_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	parent_incident nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	problem_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	change_request nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	opened_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_worked nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- NID_QA.dbo.incident_sla definition

-- Drop table

-- DROP TABLE NID_QA.dbo.incident_sla;

CREATE TABLE NID_QA.dbo.incident_sla (
	pause_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	pause_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	timezone nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_time_left nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_left nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	percentage nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	original_breach_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_percentage nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	end_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_mod_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_pause_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sla nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_tags nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_rpt_tempo_decorrido nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	schedule nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	start_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	stage nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	planned_end_time nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	has_breached nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_sla nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_schedule nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_created_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_updated_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- NID_QA.dbo.incident_task definition

-- Drop table

-- DROP TABLE NID_QA.dbo.incident_task;

CREATE TABLE NID_QA.dbo.incident_task (
	parent nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	watch_list nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_tempo_indisponivel nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	upon_reject nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	approval_history nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	skills nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	number nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_contact_attempt nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_detalhe_subcategoria_de_produto_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_codigo_reserva nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_cliente_detrator nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	state nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_designa_o_lp nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	knowledge nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[order] nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_rma nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	cmdb_ci nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	delivery_plan nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_carimbo_certificacao_remota nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	contract nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	impact nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_ordem_de_venda nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	work_notes_list nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_solicitacao_envio_equipamento_defeituoso nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	priority nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_domain_path nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	group_list nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_nome_fabricante nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_motivo nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	approval_set nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_in_cio nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_opened_month nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	needs_attention nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	universal_request nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	short_description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_entrega_cliente nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	correlation_display nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	delivery_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	work_start nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_complaint nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	additional_assignee_list nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_current_activity nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_fabricante nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_part_number_retirado nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_produto nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	service_offering nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_class_name nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	closed_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	follow_up nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_operadora_integrador nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_case_encerrado nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_follow_up_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	reassignment_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_cmdb_ci nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	assigned_to nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_acionamento nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sla_due nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_ticket_fabricante nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_visita_tecnica nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	agile_story nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_outro_fabricante nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	escalation nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	upon_approval nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_inicio_sprint nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	correlation_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_nome_produto nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_protocolo nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_sub_categoria_de_causa_raiz nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	made_sla nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_retirada nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_serial_number_retirado nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_codigo_de_rastreio nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	task_effective_number nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_de_entrega nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	opened_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_assigned_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	user_input nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_domain nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_task_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_instalacao nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_carimbo_prazo_reparo nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	route_reason nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_serial_number nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_validacao_configuracao nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_categoria_de_prooduto_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	closed_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_validacao_estoque nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_saida_site nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sn_ind_tsm_core_stage_created nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	business_service nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_worked nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_tipo_da_tarefa nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	expected_start nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_fabricante_retirado nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_part_number nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_tempo_expurgo nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	opened_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_cmdb_ci_secundario nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_teste_funcional nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	work_end nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_outros nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_atualizacao_cmdb nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_detalhe_sub_categoria_de_causa_raiz nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	work_notes nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_follow_up_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_tipo_acionamento nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	assignment_group nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_categoria_de_causa_raiz nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_envio_nf_ups nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_total_task_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	calendar_duration nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_equipamento_entregue_ups nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_descricao_equipamento_defeituoso nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	close_notes nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_categoria_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_complaint_sub nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_detalhe_subcategoria_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	contact_type nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_efetividade nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	urgency nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_certificacao_origem nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_de_envio nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	company nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_last_contact nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_subcategoria_de_produto_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	activity_due nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_nota_fiscal nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	action_status nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_duration_of_negotiations nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_current_group nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_outros_servicos nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_data_fim nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	comments nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_task_type nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	approval nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	due_date nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_mod_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_entrada_site nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_tags nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_close_code nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	location nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_subcategoria_iot_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	incident nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_parent nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_closed_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_assigned_to nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_opened_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_sys_domain nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_assignment_group nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_company nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_incident nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_created_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_updated_at nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- NID_QA.dbo.servicenow_execution_log definition

-- Drop table

-- DROP TABLE NID_QA.dbo.servicenow_execution_log;

CREATE TABLE NID_QA.dbo.servicenow_execution_log (
	id int IDENTITY(1,1) NOT NULL,
	execution_id uniqueidentifier DEFAULT newid() NULL,
	execution_type varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	start_date date NULL,
	end_date date NULL,
	started_at datetime2 DEFAULT getdate() NULL,
	ended_at datetime2 NULL,
	duration_seconds decimal(10,2) NULL,
	status varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	json_storage_enabled bit DEFAULT 0 NULL,
	total_api_requests int DEFAULT 0 NULL,
	failed_api_requests int DEFAULT 0 NULL,
	total_api_time_seconds decimal(10,2) DEFAULT 0 NULL,
	api_success_rate decimal(5,2) DEFAULT 0 NULL,
	total_db_transactions int DEFAULT 0 NULL,
	total_records_processed int DEFAULT 0 NULL,
	db_time_seconds decimal(10,2) DEFAULT 0 NULL,
	json_size_kb decimal(12,2) NULL,
	compressed_size_kb decimal(12,2) NULL,
	compression_ratio decimal(5,2) NULL,
	tables_processed varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	error_message nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	records_by_table nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	hostname varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT host_name() NULL,
	username varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT suser_sname() NULL,
	created_at datetime2 DEFAULT getdate() NULL,
	CONSTRAINT PK__servicen__3213E83FB586D910 PRIMARY KEY (id)
);
 CREATE NONCLUSTERED INDEX IX_execution_log_date_type ON dbo.servicenow_execution_log (  execution_type ASC  , start_date ASC  , end_date ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX IX_execution_log_status ON dbo.servicenow_execution_log (  status ASC  , started_at DESC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;

-- NID_QA.dbo.sys_company definition

-- Drop table

-- DROP TABLE NID_QA.dbo.sys_company;

CREATE TABLE NID_QA.dbo.sys_company (
	sys_id nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	name nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	parent nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	customer bit DEFAULT 0 NULL,
	vendor bit DEFAULT 0 NULL,
	manufacturer bit DEFAULT 0 NULL,
	phone nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fax nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	website nvarchar(1024) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	street nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	city nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	state nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	zip nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	country nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	federal_tax_id nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active bit DEFAULT 1 NULL,
	sys_created_on datetime2 NULL,
	sys_created_by nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on datetime2 NULL,
	sys_updated_by nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_created_at datetime2 DEFAULT getdate() NULL,
	etl_updated_at datetime2 DEFAULT getdate() NULL,
	etl_hash nvarchar(64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__sys_comp__8A08B5C1C212473B PRIMARY KEY (sys_id)
);
 CREATE NONCLUSTERED INDEX IX_sys_company_active ON dbo.sys_company (  active ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX IX_sys_company_name ON dbo.sys_company (  name ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;

-- NID_QA.dbo.sys_user definition

-- Drop table

-- DROP TABLE NID_QA.dbo.sys_user;

CREATE TABLE NID_QA.dbo.sys_user (
	sys_id nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	user_name nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	name nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	first_name nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	last_name nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	middle_name nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	email nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	phone nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	mobile_phone nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	company nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	department nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	location nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	manager nvarchar(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	title nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	active bit DEFAULT 1 NULL,
	locked_out bit DEFAULT 0 NULL,
	web_service_access_only bit DEFAULT 0 NULL,
	last_login datetime2 NULL,
	last_login_time datetime2 NULL,
	failed_attempts int DEFAULT 0 NULL,
	time_zone nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	date_format nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_format nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on datetime2 NULL,
	sys_created_by nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on datetime2 NULL,
	sys_updated_by nvarchar(40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	etl_created_at datetime2 DEFAULT getdate() NULL,
	etl_updated_at datetime2 DEFAULT getdate() NULL,
	etl_hash nvarchar(64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__sys_user__8A08B5C114996C15 PRIMARY KEY (sys_id)
);
 CREATE NONCLUSTERED INDEX IX_sys_user_active ON dbo.sys_user (  active ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX IX_sys_user_company ON dbo.sys_user (  company ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX IX_sys_user_email ON dbo.sys_user (  email ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;
 CREATE NONCLUSTERED INDEX IX_sys_user_username ON dbo.sys_user (  user_name ASC  )  
	 WITH (  PAD_INDEX = OFF ,FILLFACTOR = 100  ,SORT_IN_TEMPDB = OFF , IGNORE_DUP_KEY = OFF , STATISTICS_NORECOMPUTE = OFF , ONLINE = OFF , ALLOW_ROW_LOCKS = ON , ALLOW_PAGE_LOCKS = ON  )
	 ON [PRIMARY ] ;

-- NID_QA.dbo.task_time_worked definition

-- Drop table

-- DROP TABLE NID_QA.dbo.task_time_worked;

CREATE TABLE NID_QA.dbo.task_time_worked (
	comments nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	work_date nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_card nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_state nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_mod_count nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_tags nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_worked nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_id nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	time_in_seconds nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_updated_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_on nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	category nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[user] nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	sys_created_by nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	u_horas_billable nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_task nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dv_user nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);