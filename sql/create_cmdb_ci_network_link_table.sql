-- Criação da tabela cmdb_ci_network_link conforme o model `CmdbCiNetworkLink`
-- Banco: SQL Server (dbo.cmdb_ci_network_link)

IF OBJECT_ID('dbo.cmdb_ci_network_link', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.cmdb_ci_network_link (
        sys_id VARCHAR(32) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NULL,
        sys_class_name VARCHAR(255) NULL,
        u_link_name VARCHAR(255) NULL,
        u_end_a VARCHAR(100) NULL,
        u_end_b VARCHAR(100) NULL,
        u_bandwidth VARCHAR(100) NULL,
        u_status VARCHAR(100) NULL,
        u_provider VARCHAR(255) NULL,
        u_type VARCHAR(100) NULL,
        sys_created_on DATETIME2 NULL,
        sys_created_by VARCHAR(40) NULL,
        sys_updated_on DATETIME2 NULL,
        sys_updated_by VARCHAR(40) NULL,
        etl_created_at DATETIME2 NULL,
        etl_updated_at DATETIME2 NULL,
        etl_hash VARCHAR(64) NULL
    );

    -- Índices úteis
    CREATE INDEX IX_cmdb_ci_network_link_sys_updated_on ON dbo.cmdb_ci_network_link(sys_updated_on);
    CREATE INDEX IX_cmdb_ci_network_link_name ON dbo.cmdb_ci_network_link(name);
    CREATE INDEX IX_cmdb_ci_network_link_endpoints ON dbo.cmdb_ci_network_link(u_end_a, u_end_b);
END
ELSE
BEGIN
    PRINT 'A tabela dbo.cmdb_ci_network_link já existe.';
END
