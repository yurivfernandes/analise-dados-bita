-- Script para criar a tabela ast_contract
-- Tabela para armazenar contratos de ativos do ServiceNow

CREATE TABLE ast_contract (
    -- Campos padrão do sistema ServiceNow
    sys_id NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS PRIMARY KEY NOT NULL,
    sys_created_on NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_created_by NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_updated_on NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_updated_by NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_mod_count NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_class_name NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_domain NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_domain_path NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_tags NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_update_name NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_overrides NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    sys_policy NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos específicos do contrato
    number NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    name NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    active NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    state NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    type NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    description NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Datas do contrato
    start_date NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    end_date NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    effective_date NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    expiry_date NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Valores financeiros
    amount NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    payment_amount NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Relacionamentos
    vendor NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    vendor_contact NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    vendor_manager NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    contract_administrator NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    user_contact NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    stakeholder NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Termos contratuais
    terms NVARCHAR(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    license_type NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    renewal_option NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    renewal_notice_period_days NVARCHAR(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos de aprovação
    approval NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    approval_group NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    approver NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos de localização e departamento
    location NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    department NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    cost_center NVARCHAR(32) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos de tracking e status
    tracking_number NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    contract_status NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos de workflow
    workflow_state NVARCHAR(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    
    -- Campos display value (dv_) para relacionamentos
    dv_vendor NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_vendor_contact NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_vendor_manager NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_contract_administrator NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_user_contact NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_stakeholder NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_approval_group NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_approver NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_location NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_department NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_cost_center NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
    dv_sys_domain NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
);

-- Criar índices para otimizar consultas
CREATE INDEX IX_ast_contract_sys_updated_on ON ast_contract(sys_updated_on);
CREATE INDEX IX_ast_contract_vendor ON ast_contract(vendor);
CREATE INDEX IX_ast_contract_state ON ast_contract(state);
CREATE INDEX IX_ast_contract_active ON ast_contract(active);
CREATE INDEX IX_ast_contract_start_date ON ast_contract(start_date);
CREATE INDEX IX_ast_contract_end_date ON ast_contract(end_date);

-- Comentários da tabela
EXEC sp_addextendedproperty 
    @name = N'MS_Description', 
    @value = N'Tabela de contratos de ativos do ServiceNow', 
    @level0type = N'SCHEMA', @level0name = N'dbo', 
    @level1type = N'TABLE', @level1name = N'ast_contract';