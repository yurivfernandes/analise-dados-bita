-- Script para criar a tabela f_interface_traffic no SQL Server
-- Local: src/capacity_datacenter/models -> f_interface_traffic
-- Observações:
--  - id INT IDENTITY(1,1) PRIMARY KEY para corresponder ao comportamento do Django
--  - Campos mapeados conforme convenção do projeto
--  - Acrescenta colunas de auditoria ([created_at], [updated_at], [user])

SET NOCOUNT ON;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[f_interface_traffic]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[f_interface_traffic](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [node_id] VARCHAR(100) NULL,
        [date] DATE NULL,
        [in_average_bps] FLOAT NULL,
        [out_average_bps] FLOAT NULL
    );

    -- colunas de auditoria compatíveis com AuditMixin
    ALTER TABLE [dbo].[f_interface_traffic]
        ADD [created_at] DATETIME2 NULL,
            [updated_at] DATETIME2 NULL,
            [user] VARCHAR(255) NULL;

    -- índices para consultas por node e por data
    CREATE NONCLUSTERED INDEX IX_f_interface_traffic_node_date ON [dbo].[f_interface_traffic]([node_id], [date]);
END
GO
