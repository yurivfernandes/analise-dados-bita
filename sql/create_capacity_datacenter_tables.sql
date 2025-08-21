-- Script para criar as tabelas SQL Server correspondentes às models
-- Local: src/capacity_datacenter/models
-- Gera tabelas: d_node, d_interface, d_custom_poller_assignment, f_response_time, f_custom_poller_statistics
-- Observações:
--  - Campos foram mapeados de CharField(max_length=N) -> VARCHAR(N)
--  - TextField -> VARCHAR(MAX)
--  - Todos os campos com null=True foram mapeados como NULLABLE
--  - Cada tabela recebe uma coluna [id] INT IDENTITY(1,1) PRIMARY KEY para corresponder ao comportamento padrão do Django
--  - Não foram criadas chaves estrangeiras porque os models usam IDs em string (node_id, custom_poller_assignment_id)

SET NOCOUNT ON;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[d_node]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[d_node](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [nome_do_cliente] VARCHAR(255) NULL,
        [node_id] VARCHAR(10) NULL,
        [id_vgr] VARCHAR(7) NULL,
        [caption] VARCHAR(255) NULL,
        [description] VARCHAR(MAX) NULL,
        [automatizacao] VARCHAR(20) NULL,
        [redundancia] VARCHAR(20) NULL
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[d_interface]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[d_interface](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [node_id] VARCHAR(100) NULL,
        [interface_id] VARCHAR(100) NULL,
        [interface_name] VARCHAR(255) NULL,
        [caption] VARCHAR(255) NULL,
        [id_vgr] VARCHAR(100) NULL
    );
    CREATE NONCLUSTERED INDEX IX_d_interface_node_id ON [dbo].[d_interface]([node_id]);
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[d_custom_poller_assignment]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[d_custom_poller_assignment](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [custom_poller_assignment_id] VARCHAR(100) NULL,
        [node_id] VARCHAR(100) NULL
    );
    CREATE NONCLUSTERED INDEX IX_d_custom_poller_assignment_node_id ON [dbo].[d_custom_poller_assignment]([node_id]);
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[f_response_time]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[f_response_time](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [node_id] VARCHAR(100) NULL,
        [date_time] VARCHAR(100) NULL,
        [avg_response_time] VARCHAR(100) NULL,
        [percent_loss] VARCHAR(100) NULL
    );
    CREATE NONCLUSTERED INDEX IX_f_response_time_node_id ON [dbo].[f_response_time]([node_id]);
END
GO

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[f_custom_poller_statistics]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[f_custom_poller_statistics](
        [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [custom_poller_assignment_id] VARCHAR(100) NULL,
        [node_id] VARCHAR(100) NULL,
        [row_id] VARCHAR(100) NULL,
        [date_time] VARCHAR(100) NULL,
        [raw_status] VARCHAR(255) NULL,
        [weight] VARCHAR(100) NULL
    );
    CREATE NONCLUSTERED INDEX IX_f_custom_poller_statistics_node_id ON [dbo].[f_custom_poller_statistics]([node_id]);
    CREATE NONCLUSTERED INDEX IX_f_custom_poller_statistics_cpa_id ON [dbo].[f_custom_poller_statistics]([custom_poller_assignment_id]);
END
GO

-- Fim do script

django.db.utils.ProgrammingError: ('42000', "[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]String or binary data would be truncated in table 'CAPACITY_DATACENTER.dbo.d_node', column 'automatizacao'. Truncated value: 'PAB_TR_RONDONIA_1294'. (2628) (SQLFetch); [42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]The statement has been terminated. (3621)")