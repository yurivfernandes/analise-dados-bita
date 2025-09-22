from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class AstContract(models.Model):
    """Modelo para a tabela ast_contract do ServiceNow.

    Representa contratos de ativos do ServiceNow com campos padrão da tabela.
    """

    # Campos padrão do sistema ServiceNow
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain_path = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_update_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_overrides = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_policy = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Campos específicos do contrato
    number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    name = models.TextField(null=True, blank=True, db_collation=COLLATION)
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    type = models.TextField(null=True, blank=True, db_collation=COLLATION)
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Datas do contrato
    start_date = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    end_date = models.TextField(null=True, blank=True, db_collation=COLLATION)
    effective_date = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    expiry_date = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Valores financeiros
    amount = models.TextField(null=True, blank=True, db_collation=COLLATION)
    payment_amount = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Relacionamentos
    vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    vendor_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    vendor_manager = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract_administrator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    user_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    stakeholder = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Termos contratuais
    terms = models.TextField(null=True, blank=True, db_collation=COLLATION)
    license_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_option = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_notice_period_days = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Campos de aprovação
    approval = models.TextField(null=True, blank=True, db_collation=COLLATION)
    approval_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    approver = models.TextField(null=True, blank=True, db_collation=COLLATION)

    # Campos de localização e departamento
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    department = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Campos de tracking e status
    tracking_number = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract_status = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Campos de workflow
    workflow_state = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    # Campos display value (dv_) para relacionamentos
    dv_vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_vendor_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_vendor_manager = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_contract_administrator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_user_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_stakeholder = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_approval_group = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_approver = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_location = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_department = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )

    class Meta:
        managed = False
        db_table = "ast_contract"
