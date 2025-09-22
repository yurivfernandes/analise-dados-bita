from django.db import models

COLLATION = "SQL_Latin1_General_CP1_CI_AS"


class AstContract(models.Model):
    """Modelo para a tabela ast_contract do ServiceNow.

    Representa contratos de ativos do ServiceNow com todos os campos da tabela.
    """

    account = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_account = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    active = models.TextField(null=True, blank=True, db_collation=COLLATION)
    applicable_taxes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_applicable_taxes = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    application_model = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_application_model = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    approval_history = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    approver = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_approver = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    business_owner = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_business_owner = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    commitment = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    consumer = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_consumer = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract_administrator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_contract_administrator = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract_composite = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    contract_model = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_contract_model = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_adjustment = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_adjustment_percentage = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_adjustment_reason = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_adjustment_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_cost_adjustment_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_cost_center = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    cost_per_unit = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    discount = models.TextField(null=True, blank=True, db_collation=COLLATION)
    ends = models.TextField(null=True, blank=True, db_collation=COLLATION)
    expiration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_expiration = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    invoice_payment_terms = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_invoice_payment_terms = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    license_quantity_entitled = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    license_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_license_type = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    life_cycle_stage = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_life_cycle_stage = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    life_cycle_stage_status = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_life_cycle_stage_status = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    lifetime_cost = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_location = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    monthly_cost = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    parent_contract = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_parent_contract = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    payment_amount = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    payment_schedule = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_payment_schedule = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    po_number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    process = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_process = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    process_non_contractual_slas = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    ratecard = models.TextField(null=True, blank=True, db_collation=COLLATION)
    renewable = models.TextField(null=True, blank=True, db_collation=COLLATION)
    renewal_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_renewal_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_date = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_end_date = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_options = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_renewal_options = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sales_tax = models.TextField(null=True, blank=True, db_collation=COLLATION)
    short_description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    starts = models.TextField(null=True, blank=True, db_collation=COLLATION)
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sub_total_cost = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    substate = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_substate = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_sys_class_name = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_created_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain_path = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    sys_mod_count = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    tax_cost = models.TextField(null=True, blank=True, db_collation=COLLATION)
    tax_exempt = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    tax_rate = models.TextField(null=True, blank=True, db_collation=COLLATION)
    terms_and_conditions = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    total_cost = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_approve_post_labor = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_u_approve_post_labor = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_configuration_item = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_u_configuration_item = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_dias_spare = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_modelo = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_u_modelo = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    u_origem = models.TextField(null=True, blank=True, db_collation=COLLATION)
    u_sinalizacao_integracao = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_vendor = models.TextField(null=True, blank=True, db_collation=COLLATION)
    vendor_account = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    vendor_contract = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    yearly_cost = models.TextField(
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
        db_table = "ast_contract"
