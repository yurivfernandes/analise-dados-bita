import requests
import datetime
import pyodbc
from time import sleep


class ServiceNowExtractor:
    def __init__(self, base_url, auth, headers, sql_conn_str):
        self.base_url = base_url
        self.auth = auth
        self.headers = headers
        self.sql_conn_str = sql_conn_str

    def fetch_contract_sla(self, limit=10000):
        url = f"{self.base_url}/contract_sla"
        params = {"sysparm_limit": limit}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json().get("result", [])
    
    def fetch_groups(self, limit=10000):
        url = f"{self.base_url}/sys_user_group"
        params = {"sysparm_limit": limit}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        return response.json().get("result", [])
    
    def insert_groups_into_database(self, data):
        conn = pyodbc.connect(self.sql_conn_str)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM groups")

        insert_values = []

        for item in data:
            self.flatten_reference_fields(item)

            if not item:
                continue

            values = (
                    item.get("sys_id"),
                    item.get("name"),
                    item.get("description")
             )
            
            insert_values.append(values)

        
        cursor.executemany(
            """
            INSERT INTO groups (
                sys_id,name,description
            ) VALUES (
                ?,?,?
            )
            """,
            insert_values
            
        )

        conn.commit()
        cursor.close()
        conn.close()

    def insert_contract_into_database(self, data):
        conn = pyodbc.connect(self.sql_conn_str)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contract_sla")

        for item in data:
            self.flatten_reference_fields(item)

            if not item:
                continue

            cursor.execute(
                """
                INSERT INTO contract_sla (
                    schedule_source, relative_duration_works_on, retroactive_pause, set_start_to, timezone,
                    when_to_cancel, sys_updated_on, type, pause_condition, sys_class_name, duration,
                    sys_id, sys_updated_by, cancel_condition, sys_created_on, vendor, sys_domain,
                    dv_sys_domain, reset_condition, resume_condition, sys_name, reset_action,
                    flow, sys_created_by, stop_condition, start_condition, schedule_source_field,
                    workflow, dv_workflow, service_commitment, sys_mod_count, active, sys_overrides,
                    adv_condition_type, collection, sys_domain_path, sys_tags, target, schedule,
                    dv_schedule, sys_update_name, timezone_source, enable_logging, name, retroactive,
                    when_to_resume, sys_policy
                ) VALUES (
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                )
                """,
                item.get("schedule_source"),
                item.get("relative_duration_works_on"),
                item.get("retroactive_pause"),
                item.get("set_start_to"),
                item.get("timezone"),
                item.get("when_to_cancel"),
                item.get("sys_updated_on"),
                item.get("type"),
                item.get("pause_condition"),
                item.get("sys_class_name"),
                item.get("duration"),
                item.get("sys_id"),
                item.get("sys_updated_by"),
                item.get("cancel_condition"),
                item.get("sys_created_on"),
                item.get("vendor"),
                item.get("sys_domain"),
                item.get("dv_sys_domain"),
                item.get("reset_condition"),
                item.get("resume_condition"),
                item.get("sys_name"),
                item.get("reset_action"),
                item.get("flow"),
                item.get("sys_created_by"),
                item.get("stop_condition"),
                item.get("start_condition"),
                item.get("schedule_source_field"),
                item.get("workflow"),
                item.get("dv_workflow"),
                item.get("service_commitment"),
                item.get("sys_mod_count"),
                item.get("active"),
                item.get("sys_overrides"),
                item.get("adv_condition_type"),
                item.get("collection"),
                item.get("sys_domain_path"),
                item.get("sys_tags"),
                item.get("target"),
                item.get("schedule"),
                item.get("dv_schedule"),
                item.get("sys_update_name"),
                item.get("timezone_source"),
                item.get("enable_logging"),
                item.get("name"),
                item.get("retroactive"),
                item.get("when_to_resume"),
                item.get("sys_policy"),
            )
        conn.commit()
        cursor.close()
        conn.close()

    def get_incidents_by_day(self, date_str: str) -> list:

        all_incidents = []
        offset = 0
        limit = 10000
        base_url = f"{self.base_url}/incident"

        query = f"u_origemINvita_it,vita_compass,vita_fust,vgr_fleury,vgr_rd,vgr_bra,vgr^state=7^closed_at>={date_str} 00:00:00^closed_at<={date_str} 23:59:59"

        while True:
            params = {
                "sysparm_query": query,
                "sysparm_limit": limit,
                "sysparm_offset": offset,
            }

            response = requests.get(
                base_url,
                auth=self.auth,
                headers=self.headers,
                params=params,
            )

            if response.status_code != 200:
                print(
                    f"❌ Erro na requisição: {response.status_code} - {response.text}"
                )
                break

            try:
                result_page = response.json().get("result", [])
            except Exception as e:
                print(f"❌ Erro ao decodificar JSON: {e}")
                print(
                    f"Resposta parcial (até 1000 caracteres):\n{response.text[:1000]}"
                )
                break

            if not result_page:
                print("✅ Fim dos resultados.")
                break

            all_incidents.extend(result_page)
            print(f"📦 Página lida com sucesso: +{len(result_page)} registros")
            offset += limit

        print(f"✅ Total de incidentes para {date_str}: {len(all_incidents)}")
        return all_incidents


    def get_incidents_backlog(self) -> list:

        all_incidents = []
        offset = 0
        limit = 10000
        base_url = f"{self.base_url}/incident"

        query = f"u_origem=vgr^stateIN1,2,3,105"

        while True:
            params = {
                "sysparm_query": query,
                "sysparm_limit": limit,
                "sysparm_offset": offset,
            }

            response = requests.get(
                base_url,
                auth=self.auth,
                headers=self.headers,
                params=params,
            )

            if response.status_code != 200:
                print(
                    f"❌ Erro na requisição: {response.status_code} - {response.text}"
                )
                break

            try:
                result_page = response.json().get("result", [])
            except Exception as e:
                print(f"❌ Erro ao decodificar JSON: {e}")
                print(
                    f"Resposta parcial (até 1000 caracteres):\n{response.text[:1000]}"
                )
                break

            if not result_page:
                print("✅ Fim dos resultados.")
                break

            all_incidents.extend(result_page)
            print(f"📦 Página lida com sucesso: +{len(result_page)} registros")
            offset += limit

        print(f"✅ Total de incidentes para o backlog: {len(all_incidents)}")
        return all_incidents
    

    def get_tasks_for_incident(self, inc_sys_id: str):
        url = f"{self.base_url}/incident_task"
        params = {"sysparm_query": f"parent={inc_sys_id}"}
        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params
        )
        response.raise_for_status()
        return response.json().get("result", [])

    def get_slas_for_incident(self, inc_sys_id: str):
        url = f"{self.base_url}/task_sla"
        params = {"sysparm_query": f"task={inc_sys_id}", "sysparm_limit": "1000"}

        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params
        )
        response.raise_for_status()

        sla_results = response.json().get("result", [])

        return sla_results

    def get_time_worked_for_incident(self, inc_sys_id: str):
        url = f"{self.base_url}/task_time_worked"
        params = {"sysparm_query": f"task={inc_sys_id}", "sysparm_limit": "10000"}

        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params
        )
        response.raise_for_status()

        time_results = response.json().get("result", [])

        return time_results


    def flatten_reference_fields(self, inc: dict):
        for key in list(inc.keys()):
            value = inc.get(key)
            if isinstance(value, dict) and "value" in value:
                inc[key] = value.get("value")
                inc[f"dv_{key}"] = ""

    def delete_and_insert_data_backlog(
        self, incidents: list
    ):
        conn = pyodbc.connect(self.sql_conn_str)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM incident WHERE state in (1,2,3,105)")

        for inc in incidents:

            self.flatten_reference_fields(inc)

            if inc.get("company"):
                detail_url = f"{self.base_url}/core_company/{inc.get("company")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_company"] = detail.get("name", "")

            if inc.get("assignment_group"):
                detail_url = (
                    f"{self.base_url}/sys_user_group/{inc.get("assignment_group")}"
                )
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_assignment_group"] = detail.get("name", "")

            if inc.get("assigned_to"):
                detail_url = f"{self.base_url}/sys_user/{inc.get("assigned_to")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_assigned_to"] = detail.get("name", "")

            if inc.get("resolved_by"):
                detail_url = f"{self.base_url}/sys_user/{inc.get("resolved_by")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_resolved_by"] = detail.get("name", "")

            if inc.get("opened_by"):
                detail_url = f"{self.base_url}/sys_user/{inc.get("opened_by")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_opened_by"] = detail.get("name", "")

            cursor.execute(
                """INSERT INTO incident (
                    [parent], [dv_parent], [caused_by], [u_tempo_indisponivel], [sys_updated_on], [u_id_vantive], [u_nome_da_unidade], [u_cidade], [state], [sys_created_by], [u_severidade_do_chamado], [u_duration], [impact], [u_tipo_de_negocio], [u_rpt_tempo_de_abertura_encerramento], [u_cnpj], [correlation_display], [u_detalhe_solucoes], [u_detalhe_sub_categoria_da_falha], [scr_vendor], [service_offering], [parent_incident], [dv_parent_incident], [reopened_by], [u_torre_de_atendimento], [u_ip_origin], [u_anexo], [u_numero_do_contrato_voz], [u_servico_normalizado], [u_rede], [u_line], [u_telefone_do_responsavel], [scr_vendor_closed_at], [u_tempo_total_da_tratativa], [u_id_client], [correlation_id], [timeline], [u_comentarios_adicionais], [u_service_type], [u_contato_nome], [u_contato_email], [u_signal_rule_description], [u_origem], [u_endereco_do_ponto], [u_rpt_tempo_de_processamento_da_automacao_ate_abertura_do_ticket], [hold_reason], [u_classificacao_da_unidade], [sys_created_on], [u_nome_do_ponto], [u_serial_number], [calendar_stc], [u_company_name], [u_data_de_agendamento], [u_tipo_incidente], [closed_at], [business_impact], [u_uf], [time_worked], [u_task_acionamento], [u_integration], [u_tempo_expurgo], [u_sigla_da_unidade], [work_end], [u_id_sigla_da_unidade], [u_tipo_de_acionamento], [subcategory], [work_notes], [u_sla_tratativa], [u_product_subcategory_detail], [close_code], [assignment_group], [dv_assignment_group], [u_categoria_de_causa_raiz], [u_data_normalizacao_servico], [u_id_do_ponto], [u_user_agent], [u_endereco_da_unidade], [business_stc], [u_tipo_indisponibilidade], [description], [origin_id], [u_justificativa], [sys_id], [u_id_do_solicitante], [u_opening_reason], [u_fim_indisponibilidade], [u_fornecedor_cliente], [urgency], [company], [dv_company], [severity], [approval], [u_number_sigitm], [u_tempo_total_de_espera], [u_alert_name], [u_data_e_hora_da_visita_tecnica], [u_produto_n1], [sys_tags], [u_produto_n2], [u_numero_do_contrato_dados], [u_produto_n3], [u_id_da_unidade], [u_categorizacao_n3], [u_product_vivo], [u_categorizacao_n1], [scr_vendor_ticket], [u_categorizacao_n2], [u_previsao_de_atendimento], [u_categoria_da_falha], [location], [dv_location], [u_tipo_de_procedencia], [u_impact_do_ticket], [u_protocolo_fornecedor], [upon_reject], [origin_table], [approval_history], [u_b2b_downtime], [u_data_prevista_atendimento], [number], [proposed_by], [u_contatos_adicionais], [u_ip_destination], [u_serial_do_equipamento], [u_motivo_sintoma], [u_cep], [u_unidade_caixa], [u_chamado_tratado_por_analista], [u_bradesco_ci], [cmdb_ci], [dv_cmdb_ci], [contract], [u_grupo], [work_notes_list], [priority], [sys_domain_path], [u_type_ritm_or_incident], [u_justificativa_altera_o_sintoma], [business_duration], [u_tipo_do_estabelecimento], [u_detalhes_adicionais], [u_opened_month], [u_product_category], [u_descri_o_do_problema], [short_description], [u_detail_subcategory], [work_start], [u_complaint], [u_endereco_da_localidade], [u_justificativa_isolamento], [notify], [sys_class_name], [u_comment_inserted], [closed_by], [u_reincidencia], [u_expected_service_time], [u_rpt_tempo_detecao_hora], [u_cmdb_ci], [u_designador], [assigned_to], [dv_assigned_to], [u_identificacao_do_hardware], [sla_due], [upon_approval], [u_inicio_sprint], [scr_vendor_opened_at], [u_sub_categoria_de_causa_raiz], [u_designador_do_circuito], [u_sub_categoria_da_falha], [u_resolution_time], [u_ticket_sigtm_number], [child_incidents], [task_effective_number], [resolved_by], [dv_resolved_by], [u_customer_pending_time], [sys_updated_by], [opened_by], [dv_opened_by], [sys_domain], [dv_sys_domain], [proposed_on], [u_identificacao_do_ponto], [u_ticket_remedy_number], [u_observacao_da_perda_do_sla], [scr_vendor_resolved_at], [business_service], [u_hostname], [expected_start], [opened_at], [caller_id], [reopened_time], [resolved_at], [u_lp], [u_rpt_tempo_de_deteccao_do_inc_ate_a_abertura_do_ticket], [u_detalhe_sub_categoria_de_causa_raiz], [u_tipo_de_servico], [cause], [u_vendor_ticket], [calendar_duration], [u_data_e_hora_do_agendamento], [close_notes], [u_product_subcategory], [contact_type], [u_service_time], [incident_state], [problem_id], [u_procedencia], [comments], [u_link_type], [due_date], [u_nome_do_respons_vel_pela_abertura_do_chamado], [u_contato_telefone], [u_identification], [u_id_vgr], [u_case_ticket_vivo], [dv_u_case_ticket_vivo], [category]
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );""",
                inc.get("parent"),
                inc.get("dv_parent"),
                inc.get("caused_by"),
                inc.get("u_tempo_indisponivel"),
                inc.get("sys_updated_on"),
                inc.get("u_id_vantive"),
                inc.get("u_nome_da_unidade"),
                inc.get("u_cidade"),
                inc.get("state"),
                inc.get("sys_created_by"),
                inc.get("u_severidade_do_chamado"),
                inc.get("u_duration"),
                inc.get("impact"),
                inc.get("u_tipo_de_negocio"),
                inc.get("u_rpt_tempo_de_abertura_encerramento"),
                inc.get("u_cnpj"),
                inc.get("correlation_display"),
                inc.get("u_detalhe_solucoes"),
                inc.get("u_detalhe_sub_categoria_da_falha"),
                inc.get("scr_vendor"),
                inc.get("service_offering"),
                inc.get("parent_incident"),
                inc.get("dv_parent_incident"),
                inc.get("reopened_by"),
                inc.get("u_torre_de_atendimento"),
                inc.get("u_ip_origin"),
                inc.get("u_anexo"),
                inc.get("u_numero_do_contrato_voz"),
                inc.get("u_servico_normalizado"),
                inc.get("u_rede"),
                inc.get("u_line"),
                inc.get("u_telefone_do_responsavel"),
                inc.get("scr_vendor_closed_at"),
                inc.get("u_tempo_total_da_tratativa"),
                inc.get("u_id_client"),
                inc.get("correlation_id"),
                inc.get("timeline"),
                inc.get("u_comentarios_adicionais"),
                inc.get("u_service_type"),
                inc.get("u_contato_nome"),
                inc.get("u_contato_email"),
                inc.get("u_signal_rule_description"),
                inc.get("u_origem"),
                inc.get("u_endereco_do_ponto"),
                inc.get(
                    "u_rpt_tempo_de_processamento_da_automacao_ate_abertura_do_ticket"
                ),
                inc.get("hold_reason"),
                inc.get("u_classificacao_da_unidade"),
                inc.get("sys_created_on"),
                inc.get("u_nome_do_ponto"),
                inc.get("u_serial_number"),
                inc.get("calendar_stc"),
                inc.get("u_company_name"),
                inc.get("u_data_de_agendamento"),
                inc.get("u_tipo_incidente"),
                inc.get("closed_at"),
                inc.get("business_impact"),
                inc.get("u_uf"),
                inc.get("time_worked"),
                inc.get("u_task_acionamento"),
                inc.get("u_integration"),
                inc.get("u_tempo_expurgo"),
                inc.get("u_sigla_da_unidade"),
                inc.get("work_end"),
                inc.get("u_id_sigla_da_unidade"),
                inc.get("u_tipo_de_acionamento"),
                inc.get("subcategory"),
                inc.get("work_notes"),
                inc.get("u_sla_tratativa"),
                inc.get("u_product_subcategory_detail"),
                inc.get("close_code"),
                inc.get("assignment_group"),
                inc.get("dv_assignment_group"),
                inc.get("u_categoria_de_causa_raiz"),
                inc.get("u_data_normalizacao_servico"),
                inc.get("u_id_do_ponto"),
                inc.get("u_user_agent"),
                inc.get("u_endereco_da_unidade"),
                inc.get("business_stc"),
                inc.get("u_tipo_indisponibilidade"),
                inc.get("description"),
                inc.get("origin_id"),
                inc.get("u_justificativa"),
                inc.get("sys_id"),
                inc.get("u_id_do_solicitante"),
                inc.get("u_opening_reason"),
                inc.get("u_fim_indisponibilidade"),
                inc.get("u_fornecedor_cliente"),
                inc.get("urgency"),
                inc.get("company"),
                inc.get("dv_company"),
                inc.get("severity"),
                inc.get("approval"),
                inc.get("u_number_sigitm"),
                inc.get("u_tempo_total_de_espera"),
                inc.get("u_alert_name"),
                inc.get("u_data_e_hora_da_visita_tecnica"),
                inc.get("u_produto_n1"),
                inc.get("sys_tags"),
                inc.get("u_produto_n2"),
                inc.get("u_numero_do_contrato_dados"),
                inc.get("u_produto_n3"),
                inc.get("u_id_da_unidade"),
                inc.get("u_categorizacao_n3"),
                inc.get("u_product_vivo"),
                inc.get("u_categorizacao_n1"),
                inc.get("scr_vendor_ticket"),
                inc.get("u_categorizacao_n2"),
                inc.get("u_previsao_de_atendimento"),
                inc.get("u_categoria_da_falha"),
                inc.get("location"),
                inc.get("dv_location"),
                inc.get("u_tipo_de_procedencia"),
                inc.get("u_impact_do_ticket"),
                inc.get("u_protocolo_fornecedor"),
                inc.get("upon_reject"),
                inc.get("origin_table"),
                inc.get("approval_history"),
                inc.get("u_b2b_downtime"),
                inc.get("u_data_prevista_atendimento"),
                inc.get("number"),
                inc.get("proposed_by"),
                inc.get("u_contatos_adicionais"),
                inc.get("u_ip_destination"),
                inc.get("u_serial_do_equipamento"),
                inc.get("u_motivo_sintoma"),
                inc.get("u_cep"),
                inc.get("u_unidade_caixa"),
                inc.get("u_chamado_tratado_por_analista"),
                inc.get("u_bradesco_ci"),
                inc.get("cmdb_ci"),
                inc.get("dv_cmdb_ci"),
                inc.get("contract"),
                inc.get("u_grupo"),
                inc.get("work_notes_list"),
                inc.get("priority"),
                inc.get("sys_domain_path"),
                inc.get("u_type_ritm_or_incident"),
                inc.get("u_justificativa_altera_o_sintoma"),
                inc.get("business_duration"),
                inc.get("u_tipo_do_estabelecimento"),
                inc.get("u_detalhes_adicionais"),
                inc.get("u_opened_month"),
                inc.get("u_product_category"),
                inc.get("u_descri_o_do_problema"),
                inc.get("short_description"),
                inc.get("u_detail_subcategory"),
                inc.get("work_start"),
                inc.get("u_complaint"),
                inc.get("u_endereco_da_localidade"),
                inc.get("u_justificativa_isolamento"),
                inc.get("notify"),
                inc.get("sys_class_name"),
                inc.get("u_comment_inserted"),
                inc.get("closed_by"),
                inc.get("u_reincidencia"),
                inc.get("u_expected_service_time"),
                inc.get("u_rpt_tempo_detecao_hora"),
                inc.get("u_cmdb_ci"),
                inc.get("u_designador"),
                inc.get("assigned_to"),
                inc.get("dv_assigned_to"),
                inc.get("u_identificacao_do_hardware"),
                inc.get("sla_due"),
                inc.get("upon_approval"),
                inc.get("u_inicio_sprint"),
                inc.get("scr_vendor_opened_at"),
                inc.get("u_sub_categoria_de_causa_raiz"),
                inc.get("u_designador_do_circuito"),
                inc.get("u_sub_categoria_da_falha"),
                inc.get("u_resolution_time"),
                inc.get("u_ticket_sigtm_number"),
                inc.get("child_incidents"),
                inc.get("task_effective_number"),
                inc.get("resolved_by"),
                inc.get("dv_resolved_by"),
                inc.get("u_customer_pending_time"),
                inc.get("sys_updated_by"),
                inc.get("opened_by"),
                inc.get("dv_opened_by"),
                inc.get("sys_domain"),
                inc.get("dv_sys_domain"),
                inc.get("proposed_on"),
                inc.get("u_identificacao_do_ponto"),
                inc.get("u_ticket_remedy_number"),
                inc.get("u_observacao_da_perda_do_sla"),
                inc.get("scr_vendor_resolved_at"),
                inc.get("business_service"),
                inc.get("u_hostname"),
                inc.get("expected_start"),
                inc.get("opened_at"),
                inc.get("caller_id"),
                inc.get("reopened_time"),
                inc.get("resolved_at"),
                inc.get("u_lp"),
                inc.get("u_rpt_tempo_de_deteccao_do_inc_ate_a_abertura_do_ticket"),
                inc.get("u_detalhe_sub_categoria_de_causa_raiz"),
                inc.get("u_tipo_de_servico"),
                inc.get("cause"),
                inc.get("u_vendor_ticket"),
                inc.get("calendar_duration"),
                inc.get("u_data_e_hora_do_agendamento"),
                inc.get("close_notes"),
                inc.get("u_product_subcategory"),
                inc.get("contact_type"),
                inc.get("u_service_time"),
                inc.get("incident_state"),
                inc.get("problem_id"),
                inc.get("u_procedencia"),
                inc.get("comments"),
                inc.get("u_link_type"),
                inc.get("due_date"),
                inc.get("u_nome_do_respons_vel_pela_abertura_do_chamado"),
                inc.get("u_contato_telefone"),
                inc.get("u_identification"),
                inc.get("u_id_vgr"),
                inc.get("u_case_ticket_vivo"),
                inc.get("dv_u_case_ticket_vivo"),
                inc.get("category"),
            )

    def delete_and_insert_data(
        self, date: str, incidents: list, tasks: dict, slas_dict: dict
    ):
        conn = pyodbc.connect(self.sql_conn_str)
        cursor = conn.cursor()

        

        for inc in incidents:

            cursor.execute("DELETE FROM incident WHERE sys_id = ?", inc.get('sys_id'))

            self.flatten_reference_fields(inc)

            if inc.get("company"):
                detail_url = f"{self.base_url}/core_company/{inc.get("company")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_company"] = detail.get("name", "")

            # if inc.get("assignment_group"):
            #     detail_url = (
            #         f"{self.base_url}/sys_user_group/{inc.get("assignment_group")}"
            #     )
            #     response = requests.get(
            #         detail_url, auth=self.auth, headers=self.headers
            #     )
            #     if response.status_code == 200:
            #         detail = response.json().get("result", {})
            #         inc["dv_assignment_group"] = detail.get("name", "")

            # if inc.get("assigned_to"):
            #     detail_url = f"{self.base_url}/sys_user/{inc.get("assigned_to")}"
            #     response = requests.get(
            #         detail_url, auth=self.auth, headers=self.headers
            #     )
            #     if response.status_code == 200:
            #         detail = response.json().get("result", {})
            #         inc["dv_assigned_to"] = detail.get("name", "")

            if inc.get("resolved_by"):
                detail_url = f"{self.base_url}/sys_user/{inc.get("resolved_by")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_resolved_by"] = detail.get("name", "")

            if inc.get("opened_by"):
                detail_url = f"{self.base_url}/sys_user/{inc.get("opened_by")}"
                response = requests.get(
                    detail_url, auth=self.auth, headers=self.headers
                )
                if response.status_code == 200:
                    detail = response.json().get("result", {})
                    inc["dv_opened_by"] = detail.get("name", "")

            cursor.execute(
                """INSERT INTO incident (
                    [parent], [dv_parent], [caused_by], [u_tempo_indisponivel], [sys_updated_on], [u_id_vantive], [u_nome_da_unidade], [u_cidade], [state], [sys_created_by], [u_severidade_do_chamado], [u_duration], [impact], [u_tipo_de_negocio], [u_rpt_tempo_de_abertura_encerramento], [u_cnpj], [correlation_display], [u_detalhe_solucoes], [u_detalhe_sub_categoria_da_falha], [scr_vendor], [service_offering], [parent_incident], [dv_parent_incident], [reopened_by], [u_torre_de_atendimento], [u_ip_origin], [u_anexo], [u_numero_do_contrato_voz], [u_servico_normalizado], [u_rede], [u_line], [u_telefone_do_responsavel], [scr_vendor_closed_at], [u_tempo_total_da_tratativa], [u_id_client], [correlation_id], [timeline], [u_comentarios_adicionais], [u_service_type], [u_contato_nome], [u_contato_email], [u_signal_rule_description], [u_origem], [u_endereco_do_ponto], [u_rpt_tempo_de_processamento_da_automacao_ate_abertura_do_ticket], [hold_reason], [u_classificacao_da_unidade], [sys_created_on], [u_nome_do_ponto], [u_serial_number], [calendar_stc], [u_company_name], [u_data_de_agendamento], [u_tipo_incidente], [closed_at], [business_impact], [u_uf], [time_worked], [u_task_acionamento], [u_integration], [u_tempo_expurgo], [u_sigla_da_unidade], [work_end], [u_id_sigla_da_unidade], [u_tipo_de_acionamento], [subcategory], [work_notes], [u_sla_tratativa], [u_product_subcategory_detail], [close_code], [assignment_group], [dv_assignment_group], [u_categoria_de_causa_raiz], [u_data_normalizacao_servico], [u_id_do_ponto], [u_user_agent], [u_endereco_da_unidade], [business_stc], [u_tipo_indisponibilidade], [description], [origin_id], [u_justificativa], [sys_id], [u_id_do_solicitante], [u_opening_reason], [u_fim_indisponibilidade], [u_fornecedor_cliente], [urgency], [company], [dv_company], [severity], [approval], [u_number_sigitm], [u_tempo_total_de_espera], [u_alert_name], [u_data_e_hora_da_visita_tecnica], [u_produto_n1], [sys_tags], [u_produto_n2], [u_numero_do_contrato_dados], [u_produto_n3], [u_id_da_unidade], [u_categorizacao_n3], [u_product_vivo], [u_categorizacao_n1], [scr_vendor_ticket], [u_categorizacao_n2], [u_previsao_de_atendimento], [u_categoria_da_falha], [location], [dv_location], [u_tipo_de_procedencia], [u_impact_do_ticket], [u_protocolo_fornecedor], [upon_reject], [origin_table], [approval_history], [u_b2b_downtime], [u_data_prevista_atendimento], [number], [proposed_by], [u_contatos_adicionais], [u_ip_destination], [u_serial_do_equipamento], [u_motivo_sintoma], [u_cep], [u_unidade_caixa], [u_chamado_tratado_por_analista], [u_bradesco_ci], [cmdb_ci], [dv_cmdb_ci], [contract], [u_grupo], [work_notes_list], [priority], [sys_domain_path], [u_type_ritm_or_incident], [u_justificativa_altera_o_sintoma], [business_duration], [u_tipo_do_estabelecimento], [u_detalhes_adicionais], [u_opened_month], [u_product_category], [u_descri_o_do_problema], [short_description], [u_detail_subcategory], [work_start], [u_complaint], [u_endereco_da_localidade], [u_justificativa_isolamento], [notify], [sys_class_name], [u_comment_inserted], [closed_by], [u_reincidencia], [u_expected_service_time], [u_rpt_tempo_detecao_hora], [u_cmdb_ci], [u_designador], [assigned_to], [dv_assigned_to], [u_identificacao_do_hardware], [sla_due], [upon_approval], [u_inicio_sprint], [scr_vendor_opened_at], [u_sub_categoria_de_causa_raiz], [u_designador_do_circuito], [u_sub_categoria_da_falha], [u_resolution_time], [u_ticket_sigtm_number], [child_incidents], [task_effective_number], [resolved_by], [dv_resolved_by], [u_customer_pending_time], [sys_updated_by], [opened_by], [dv_opened_by], [sys_domain], [dv_sys_domain], [proposed_on], [u_identificacao_do_ponto], [u_ticket_remedy_number], [u_observacao_da_perda_do_sla], [scr_vendor_resolved_at], [business_service], [u_hostname], [expected_start], [opened_at], [caller_id], [reopened_time], [resolved_at], [u_lp], [u_rpt_tempo_de_deteccao_do_inc_ate_a_abertura_do_ticket], [u_detalhe_sub_categoria_de_causa_raiz], [u_tipo_de_servico], [cause], [u_vendor_ticket], [calendar_duration], [u_data_e_hora_do_agendamento], [close_notes], [u_product_subcategory], [contact_type], [u_service_time], [incident_state], [problem_id], [u_procedencia], [comments], [u_link_type], [due_date], [u_nome_do_respons_vel_pela_abertura_do_chamado], [u_contato_telefone], [u_identification], [u_id_vgr], [u_case_ticket_vivo], [dv_u_case_ticket_vivo], [category]
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );""",
                inc.get("parent"),
                inc.get("dv_parent"),
                inc.get("caused_by"),
                inc.get("u_tempo_indisponivel"),
                inc.get("sys_updated_on"),
                inc.get("u_id_vantive"),
                inc.get("u_nome_da_unidade"),
                inc.get("u_cidade"),
                inc.get("state"),
                inc.get("sys_created_by"),
                inc.get("u_severidade_do_chamado"),
                inc.get("u_duration"),
                inc.get("impact"),
                inc.get("u_tipo_de_negocio"),
                inc.get("u_rpt_tempo_de_abertura_encerramento"),
                inc.get("u_cnpj"),
                inc.get("correlation_display"),
                inc.get("u_detalhe_solucoes"),
                inc.get("u_detalhe_sub_categoria_da_falha"),
                inc.get("scr_vendor"),
                inc.get("service_offering"),
                inc.get("parent_incident"),
                inc.get("dv_parent_incident"),
                inc.get("reopened_by"),
                inc.get("u_torre_de_atendimento"),
                inc.get("u_ip_origin"),
                inc.get("u_anexo"),
                inc.get("u_numero_do_contrato_voz"),
                inc.get("u_servico_normalizado"),
                inc.get("u_rede"),
                inc.get("u_line"),
                inc.get("u_telefone_do_responsavel"),
                inc.get("scr_vendor_closed_at"),
                inc.get("u_tempo_total_da_tratativa"),
                inc.get("u_id_client"),
                inc.get("correlation_id"),
                inc.get("timeline"),
                inc.get("u_comentarios_adicionais"),
                inc.get("u_service_type"),
                inc.get("u_contato_nome"),
                inc.get("u_contato_email"),
                inc.get("u_signal_rule_description"),
                inc.get("u_origem"),
                inc.get("u_endereco_do_ponto"),
                inc.get(
                    "u_rpt_tempo_de_processamento_da_automacao_ate_abertura_do_ticket"
                ),
                inc.get("hold_reason"),
                inc.get("u_classificacao_da_unidade"),
                inc.get("sys_created_on"),
                inc.get("u_nome_do_ponto"),
                inc.get("u_serial_number"),
                inc.get("calendar_stc"),
                inc.get("u_company_name"),
                inc.get("u_data_de_agendamento"),
                inc.get("u_tipo_incidente"),
                inc.get("closed_at"),
                inc.get("business_impact"),
                inc.get("u_uf"),
                inc.get("time_worked"),
                inc.get("u_task_acionamento"),
                inc.get("u_integration"),
                inc.get("u_tempo_expurgo"),
                inc.get("u_sigla_da_unidade"),
                inc.get("work_end"),
                inc.get("u_id_sigla_da_unidade"),
                inc.get("u_tipo_de_acionamento"),
                inc.get("subcategory"),
                inc.get("work_notes"),
                inc.get("u_sla_tratativa"),
                inc.get("u_product_subcategory_detail"),
                inc.get("close_code"),
                inc.get("assignment_group"),
                inc.get("dv_assignment_group"),
                inc.get("u_categoria_de_causa_raiz"),
                inc.get("u_data_normalizacao_servico"),
                inc.get("u_id_do_ponto"),
                inc.get("u_user_agent"),
                inc.get("u_endereco_da_unidade"),
                inc.get("business_stc"),
                inc.get("u_tipo_indisponibilidade"),
                inc.get("description"),
                inc.get("origin_id"),
                inc.get("u_justificativa"),
                inc.get("sys_id"),
                inc.get("u_id_do_solicitante"),
                inc.get("u_opening_reason"),
                inc.get("u_fim_indisponibilidade"),
                inc.get("u_fornecedor_cliente"),
                inc.get("urgency"),
                inc.get("company"),
                inc.get("dv_company"),
                inc.get("severity"),
                inc.get("approval"),
                inc.get("u_number_sigitm"),
                inc.get("u_tempo_total_de_espera"),
                inc.get("u_alert_name"),
                inc.get("u_data_e_hora_da_visita_tecnica"),
                inc.get("u_produto_n1"),
                inc.get("sys_tags"),
                inc.get("u_produto_n2"),
                inc.get("u_numero_do_contrato_dados"),
                inc.get("u_produto_n3"),
                inc.get("u_id_da_unidade"),
                inc.get("u_categorizacao_n3"),
                inc.get("u_product_vivo"),
                inc.get("u_categorizacao_n1"),
                inc.get("scr_vendor_ticket"),
                inc.get("u_categorizacao_n2"),
                inc.get("u_previsao_de_atendimento"),
                inc.get("u_categoria_da_falha"),
                inc.get("location"),
                inc.get("dv_location"),
                inc.get("u_tipo_de_procedencia"),
                inc.get("u_impact_do_ticket"),
                inc.get("u_protocolo_fornecedor"),
                inc.get("upon_reject"),
                inc.get("origin_table"),
                inc.get("approval_history"),
                inc.get("u_b2b_downtime"),
                inc.get("u_data_prevista_atendimento"),
                inc.get("number"),
                inc.get("proposed_by"),
                inc.get("u_contatos_adicionais"),
                inc.get("u_ip_destination"),
                inc.get("u_serial_do_equipamento"),
                inc.get("u_motivo_sintoma"),
                inc.get("u_cep"),
                inc.get("u_unidade_caixa"),
                inc.get("u_chamado_tratado_por_analista"),
                inc.get("u_bradesco_ci"),
                inc.get("cmdb_ci"),
                inc.get("dv_cmdb_ci"),
                inc.get("contract"),
                inc.get("u_grupo"),
                inc.get("work_notes_list"),
                inc.get("priority"),
                inc.get("sys_domain_path"),
                inc.get("u_type_ritm_or_incident"),
                inc.get("u_justificativa_altera_o_sintoma"),
                inc.get("business_duration"),
                inc.get("u_tipo_do_estabelecimento"),
                inc.get("u_detalhes_adicionais"),
                inc.get("u_opened_month"),
                inc.get("u_product_category"),
                inc.get("u_descri_o_do_problema"),
                inc.get("short_description"),
                inc.get("u_detail_subcategory"),
                inc.get("work_start"),
                inc.get("u_complaint"),
                inc.get("u_endereco_da_localidade"),
                inc.get("u_justificativa_isolamento"),
                inc.get("notify"),
                inc.get("sys_class_name"),
                inc.get("u_comment_inserted"),
                inc.get("closed_by"),
                inc.get("u_reincidencia"),
                inc.get("u_expected_service_time"),
                inc.get("u_rpt_tempo_detecao_hora"),
                inc.get("u_cmdb_ci"),
                inc.get("u_designador"),
                inc.get("assigned_to"),
                inc.get("dv_assigned_to"),
                inc.get("u_identificacao_do_hardware"),
                inc.get("sla_due"),
                inc.get("upon_approval"),
                inc.get("u_inicio_sprint"),
                inc.get("scr_vendor_opened_at"),
                inc.get("u_sub_categoria_de_causa_raiz"),
                inc.get("u_designador_do_circuito"),
                inc.get("u_sub_categoria_da_falha"),
                inc.get("u_resolution_time"),
                inc.get("u_ticket_sigtm_number"),
                inc.get("child_incidents"),
                inc.get("task_effective_number"),
                inc.get("resolved_by"),
                inc.get("dv_resolved_by"),
                inc.get("u_customer_pending_time"),
                inc.get("sys_updated_by"),
                inc.get("opened_by"),
                inc.get("dv_opened_by"),
                inc.get("sys_domain"),
                inc.get("dv_sys_domain"),
                inc.get("proposed_on"),
                inc.get("u_identificacao_do_ponto"),
                inc.get("u_ticket_remedy_number"),
                inc.get("u_observacao_da_perda_do_sla"),
                inc.get("scr_vendor_resolved_at"),
                inc.get("business_service"),
                inc.get("u_hostname"),
                inc.get("expected_start"),
                inc.get("opened_at"),
                inc.get("caller_id"),
                inc.get("reopened_time"),
                inc.get("resolved_at"),
                inc.get("u_lp"),
                inc.get("u_rpt_tempo_de_deteccao_do_inc_ate_a_abertura_do_ticket"),
                inc.get("u_detalhe_sub_categoria_de_causa_raiz"),
                inc.get("u_tipo_de_servico"),
                inc.get("cause"),
                inc.get("u_vendor_ticket"),
                inc.get("calendar_duration"),
                inc.get("u_data_e_hora_do_agendamento"),
                inc.get("close_notes"),
                inc.get("u_product_subcategory"),
                inc.get("contact_type"),
                inc.get("u_service_time"),
                inc.get("incident_state"),
                inc.get("problem_id"),
                inc.get("u_procedencia"),
                inc.get("comments"),
                inc.get("u_link_type"),
                inc.get("due_date"),
                inc.get("u_nome_do_respons_vel_pela_abertura_do_chamado"),
                inc.get("u_contato_telefone"),
                inc.get("u_identification"),
                inc.get("u_id_vgr"),
                inc.get("u_case_ticket_vivo"),
                inc.get("dv_u_case_ticket_vivo"),
                inc.get("category"),
            )

            inc_id = inc.get("sys_id")
            if inc_id:
                tasks = self.get_tasks_for_incident(inc_id)

            for task in tasks:

                self.flatten_reference_fields(task)

                task["incident"] = inc.get("sys_id")
                task["dv_incident"] = inc.get("number")

                if task.get("closed_by"):
                    detail_url = f"{self.base_url}/sys_user/{task.get("closed_by")}"
                    response = requests.get(
                        detail_url, auth=self.auth, headers=self.headers
                    )
                    if response.status_code == 200:
                        detail = response.json().get("result", {})
                        task["dv_closed_by"] = detail.get("name", "")

                if task.get("assigned_to"):
                    detail_url = f"{self.base_url}/sys_user/{task.get("assigned_to")}"
                    response = requests.get(
                        detail_url, auth=self.auth, headers=self.headers
                    )
                    if response.status_code == 200:
                        detail = response.json().get("result", {})
                        task["dv_assigned_to"] = detail.get("name", "")

                if task.get("opened_by"):
                    detail_url = f"{self.base_url}/sys_user/{task.get("opened_by")}"
                    response = requests.get(
                        detail_url, auth=self.auth, headers=self.headers
                    )
                    if response.status_code == 200:
                        detail = response.json().get("result", {})
                        task["dv_opened_by"] = detail.get("name", "")

                cursor.execute(
                    "DELETE FROM incident_task WHERE sys_id = ?", task.get("sys_id")
                )

                cursor.execute(
                    "INSERT INTO incident_task ([u_tempo_indisponivel], [sys_updated_on], [number], [u_contact_attempt], [u_detalhe_subcategoria_de_produto_iot_task], [state], [u_designa_o_lp], [sys_created_by], [u_rma], [u_duration], [cmdb_ci], [delivery_plan], [contract], [impact], [u_ordem_de_venda], [work_notes_list], [u_data_solicitacao_envio_equipamento_defeituoso], [priority], [business_duration], [group_list], [u_nome_fabricante], [u_motivo], [u_data_in_cio], [u_opened_month], [u_data_entrega_cliente], [correlation_display], [delivery_task], [work_start], [u_complaint], [additional_assignee_list], [u_produto], [service_offering], [sys_class_name], [closed_by], [dv_closed_by], [u_operadora_integrador], [u_data_case_encerrado], [u_cmdb_ci], [assigned_to], [dv_assigned_to], [u_acionamento], [sla_due], [u_ticket_fabricante], [u_visita_tecnica], [u_outro_fabricante], [u_inicio_sprint], [correlation_id], [u_protocolo], [made_sla], [u_codigo_de_rastreio], [task_effective_number], [sys_updated_by], [u_data_de_entrega], [opened_by], [dv_opened_by], [u_assigned_duration], [user_input], [sys_created_on], [u_task_duration], [u_carimbo_prazo_reparo], [route_reason], [u_serial_number], [u_data_validacao_configuracao], [u_categoria_de_prooduto_iot_task], [closed_at], [u_data_validacao_estoque], [u_saida_site], [sn_ind_tsm_core_stage_created], [business_service], [time_worked], [u_tipo_da_tarefa], [expected_start], [u_part_number], [u_tempo_expurgo], [opened_at], [u_cmdb_ci_secundario], [u_data_teste_funcional], [work_end], [u_outros], [work_notes], [u_follow_up_count], [u_tipo_acionamento], [u_data_envio_nf_ups], [u_total_task_duration], [calendar_duration], [u_data_equipamento_entregue_ups], [u_categoria_iot_task], [u_complaint_sub], [u_detalhe_subcategoria_iot_task], [sys_id], [contact_type], [u_efetividade], [urgency], [u_data_de_envio], [u_last_contact], [u_subcategoria_de_produto_iot_task], [activity_due], [u_nota_fiscal], [action_status], [u_duration_of_negotiations], [u_current_group], [u_data_fim], [comments], [u_task_type], [due_date], [u_entrada_site], [sys_tags], [u_close_code], [location], [incident], [dv_incident]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    task.get("u_tempo_indisponivel"),
                    task.get("sys_updated_on"),
                    task.get("number"),
                    task.get("u_contact_attempt"),
                    task.get("u_detalhe_subcategoria_de_produto_iot_task"),
                    task.get("state"),
                    task.get("u_designa_o_lp"),
                    task.get("sys_created_by"),
                    task.get("u_rma"),
                    task.get("u_duration"),
                    task.get("cmdb_ci"),
                    task.get("delivery_plan"),
                    task.get("contract"),
                    task.get("impact"),
                    task.get("u_ordem_de_venda"),
                    task.get("work_notes_list"),
                    task.get("u_data_solicitacao_envio_equipamento_defeituoso"),
                    task.get("priority"),
                    task.get("business_duration"),
                    task.get("group_list"),
                    task.get("u_nome_fabricante"),
                    task.get("u_motivo"),
                    task.get("u_data_in_cio"),
                    task.get("u_opened_month"),
                    task.get("u_data_entrega_cliente"),
                    task.get("correlation_display"),
                    task.get("delivery_task"),
                    task.get("work_start"),
                    task.get("u_complaint"),
                    task.get("additional_assignee_list"),
                    task.get("u_produto"),
                    task.get("service_offering"),
                    task.get("sys_class_name"),
                    task.get("closed_by"),
                    task.get("dv_closed_by"),
                    task.get("u_operadora_integrador"),
                    task.get("u_data_case_encerrado"),
                    task.get("u_cmdb_ci"),
                    task.get("assigned_to"),
                    task.get("dv_assigned_to"),
                    task.get("u_acionamento"),
                    task.get("sla_due"),
                    task.get("u_ticket_fabricante"),
                    task.get("u_visita_tecnica"),
                    task.get("u_outro_fabricante"),
                    task.get("u_inicio_sprint"),
                    task.get("correlation_id"),
                    task.get("u_protocolo"),
                    task.get("made_sla"),
                    task.get("u_codigo_de_rastreio"),
                    task.get("task_effective_number"),
                    task.get("sys_updated_by"),
                    task.get("u_data_de_entrega"),
                    task.get("opened_by"),
                    task.get("dv_opened_by"),
                    task.get("u_assigned_duration"),
                    task.get("user_input"),
                    task.get("sys_created_on"),
                    task.get("u_task_duration"),
                    task.get("u_carimbo_prazo_reparo"),
                    task.get("route_reason"),
                    task.get("u_serial_number"),
                    task.get("u_data_validacao_configuracao"),
                    task.get("u_categoria_de_prooduto_iot_task"),
                    task.get("closed_at"),
                    task.get("u_data_validacao_estoque"),
                    task.get("u_saida_site"),
                    task.get("sn_ind_tsm_core_stage_created"),
                    task.get("business_service"),
                    task.get("time_worked"),
                    task.get("u_tipo_da_tarefa"),
                    task.get("expected_start"),
                    task.get("u_part_number"),
                    task.get("u_tempo_expurgo"),
                    task.get("opened_at"),
                    task.get("u_cmdb_ci_secundario"),
                    task.get("u_data_teste_funcional"),
                    task.get("work_end"),
                    task.get("u_outros"),
                    task.get("work_notes"),
                    task.get("u_follow_up_count"),
                    task.get("u_tipo_acionamento"),
                    task.get("u_data_envio_nf_ups"),
                    task.get("u_total_task_duration"),
                    task.get("calendar_duration"),
                    task.get("u_data_equipamento_entregue_ups"),
                    task.get("u_categoria_iot_task"),
                    task.get("u_complaint_sub"),
                    task.get("u_detalhe_subcategoria_iot_task"),
                    task.get("sys_id"),
                    task.get("contact_type"),
                    task.get("u_efetividade"),
                    task.get("urgency"),
                    task.get("u_data_de_envio"),
                    task.get("u_last_contact"),
                    task.get("u_subcategoria_de_produto_iot_task"),
                    task.get("activity_due"),
                    task.get("u_nota_fiscal"),
                    task.get("action_status"),
                    task.get("u_duration_of_negotiations"),
                    task.get("u_current_group"),
                    task.get("u_data_fim"),
                    task.get("comments"),
                    task.get("u_task_type"),
                    task.get("due_date"),
                    task.get("u_entrada_site"),
                    task.get("sys_tags"),
                    task.get("u_close_code"),
                    task.get("location"),
                    task.get("incident"),
                    "",
                )

            inc_id = inc.get("sys_id")
            if inc_id:
                slas = self.get_slas_for_incident(inc_id)

            for sla in slas:

                self.flatten_reference_fields(sla)

                sla_sys_id = sla.get("sla")
                sla_name = ""

                # if sla_sys_id:
                #     sla_detail_url = f"{self.base_url}/contract_sla/{sla_sys_id}"
                #     sla_response = requests.get(
                #         sla_detail_url, auth=self.auth, headers=self.headers
                #     )
                #     if sla_response.status_code == 200:
                #         sla_detail = sla_response.json().get("result", {})
                #         sla_name = sla_detail.get("name", "")

                sla["dv_sla"] = ""

                sla["incident"] = inc.get("sys_id")
                sla["dv_incident"] = inc.get("number")

                cursor.execute(
                    "DELETE FROM incident_sla WHERE sys_id = ?", sla.get("sys_id")
                )

                cursor.execute(
                    "INSERT INTO incident_sla (incident,dv_incident,[pause_duration], [pause_time], [timezone], [sys_updated_on], [business_time_left], [duration], [sys_id], [time_left], [sys_updated_by], [sys_created_on], [percentage], [original_breach_time], [sys_created_by], [business_percentage], [end_time], [sys_mod_count], [active], [business_pause_duration], [sla], [dv_sla], [sys_tags], [u_rpt_tempo_decorrido], [schedule], [dv_schedule], [start_time], [business_duration], [task], [dv_task], [stage], [planned_end_time], [has_breached]) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                    sla.get("incident"),
                    sla.get("dv_incident"),
                    sla.get("pause_duration"),
                    sla.get("pause_time"),
                    sla.get("timezone"),
                    sla.get("sys_updated_on"),
                    sla.get("business_time_left"),
                    sla.get("duration"),
                    sla.get("sys_id"),
                    sla.get("time_left"),
                    sla.get("sys_updated_by"),
                    sla.get("sys_created_on"),
                    sla.get("percentage"),
                    sla.get("original_breach_time"),
                    sla.get("sys_created_by"),
                    sla.get("business_percentage"),
                    sla.get("end_time"),
                    sla.get("sys_mod_count"),
                    sla.get("active"),
                    sla.get("business_pause_duration"),
                    sla.get("sla"),
                    sla.get("dv_sla"),
                    sla.get("sys_tags"),
                    sla.get("u_rpt_tempo_decorrido"),
                    sla.get("schedule"),
                    sla.get("dv_schedule"),
                    sla.get("start_time"),
                    sla.get("business_duration"),
                    sla.get("task"),
                    sla.get("dv_task"),
                    sla.get("stage"),
                    sla.get("planned_end_time"),
                    sla.get("has_breached"),
                )

            inc_id = inc.get("sys_id")
            if inc_id:
                times = self.get_time_worked_for_incident(inc_id)

            for time in times:

                self.flatten_reference_fields(time)
              

                time["incident"] = inc.get("sys_id")
                time["dv_incident"] = inc.get("number")

                cursor.execute(
                    "DELETE FROM time_worked WHERE sys_id = ?", time.get("sys_id")
                )

                cursor.execute(
                    "INSERT INTO time_worked (incident,	dv_incident,	comments,	work_date,	time_card,	u_state,	sys_mod_count,	sys_updated_on,	sys_tags,	time_worked,	sys_id,	time_in_seconds,	sys_updated_by,	task,	dv_task,	sys_created_on,	category,	[user],	dv_user,	sys_created_by,	u_horas_billable) VALUES (?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?,	?)",
                    time.get('incident'),
                    time.get('dv_incident'),
                    time.get('comments'),
                    time.get('work_date'),
                    time.get('time_card'),
                    time.get('u_state'),
                    time.get('sys_mod_count'),
                    time.get('sys_updated_on'),
                    time.get('sys_tags'),
                    time.get('time_worked'),
                    time.get('sys_id'),
                    time.get('time_in_seconds'),
                    time.get('sys_updated_by'),
                    time.get('task'),
                    time.get('dv_task'),
                    time.get('sys_created_on'),
                    time.get('category'),
                    time.get('user'),
                    time.get('dv_user'),
                    time.get('sys_created_by'),
                    time.get('u_horas_billable')


                )
        conn.commit()
        cursor.close()
        conn.close()

    def run(self):

        sla_data = self.fetch_contract_sla()
        self.insert_contract_into_database(sla_data)

        groups = self.fetch_groups()
        self.insert_groups_into_database(groups)

        print(f"- Contrato importado")

        today = datetime.datetime.now().date()
        print (f"*** INICIO: {datetime.datetime.now()}")
        for i in range(3, -1, -1):  # dois dias atrás até hoje
            day = today - datetime.timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")

            print(f"📅 Processando dia: {date_str}")
            incidents = self.get_incidents_by_day(date_str)

            slas_dict = {}
            tasks = {}

            # for inc in incidents:
            #     inc_id = inc.get("sys_id")
            #     if inc_id:
            #         tasks = self.get_tasks_for_incident(inc_id)
            #         # slas = self.get_slas_for_incident(inc_id)
            #         # slas_dict[inc_id] = slas
            #         sleep(0.2)  # evita overload na API

            self.delete_and_insert_data(date_str, incidents, tasks, slas_dict)
            print(f"✅ Finalizado dia: {date_str}\n")

        # print(f"📅 Processando o backlog")
        # incidents = self.get_incidents_backlog()
        # self.delete_and_insert_data_backlog(incidents)
        # print(f"✅ Finalizado backlog")

        print (f"*** FIM: {datetime.datetime.now()}")


if __name__ == "__main__":
    servicenow_base_url = "https://vivob2b.service-now.com/api/now/table"
    servicenow_username = "integrationUserDev"
    servicenow_password = "i5jz@Lo1+q5^!x4"

    auth = (servicenow_username, servicenow_password)
    headers = {"Content-Type": "application/json"}
    sql_conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.21.0.6;DATABASE=API_SERVICE_NOW;UID=usr_rafael;PWD=Industri@l31"
    extractor = ServiceNowExtractor(servicenow_base_url, auth, headers, sql_conn_str)
    extractor.run()