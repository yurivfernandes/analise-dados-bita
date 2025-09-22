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
    active = models.BooleanField(null=True, blank=True)
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
    commitment = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
    cost_adjustment = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    cost_adjustment_percentage = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
    cost_per_unit = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    discount = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    ends = models.DateField(null=True, blank=True)
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
    license_quantity_entitled = models.IntegerField(null=True, blank=True)
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
    lifetime_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    location = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_location = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    monthly_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    number = models.TextField(null=True, blank=True, db_collation=COLLATION)
    parent_contract = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_parent_contract = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    payment_amount = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
    process_non_contractual_slas = models.BooleanField(null=True, blank=True)
    ratecard = models.BooleanField(null=True, blank=True)
    renewable = models.BooleanField(null=True, blank=True)
    renewal_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_renewal_contact = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    renewal_date = models.DateField(null=True, blank=True)
    renewal_end_date = models.DateField(null=True, blank=True)
    renewal_options = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    dv_renewal_options = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sales_tax = models.BooleanField(null=True, blank=True)
    short_description = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    starts = models.DateField(null=True, blank=True)
    state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    dv_state = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sub_total_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
    sys_created_on = models.DateTimeField(null=True, blank=True)
    sys_domain = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_domain_path = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_id = models.TextField(primary_key=True, db_collation=COLLATION)
    sys_mod_count = models.IntegerField(null=True, blank=True)
    sys_tags = models.TextField(null=True, blank=True, db_collation=COLLATION)
    sys_updated_by = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    sys_updated_on = models.DateTimeField(null=True, blank=True)
    tax_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    tax_exempt = models.BooleanField(null=True, blank=True)
    tax_rate = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
    )
    terms_and_conditions = models.TextField(
        null=True, blank=True, db_collation=COLLATION
    )
    total_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
    u_dias_spare = models.IntegerField(null=True, blank=True)
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
    yearly_cost = models.DecimalField(
        max_digits=18, decimal_places=0, null=True, blank=True
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
