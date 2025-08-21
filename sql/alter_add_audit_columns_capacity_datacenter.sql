-- Script para adicionar colunas de auditoria (created_at, updated_at, user)
-- Aplica-se às tabelas: d_node, d_interface, d_custom_poller_assignment, f_response_time, f_custom_poller_statistics
SET NOCOUNT ON;

DECLARE @table SYSNAME;
DECLARE @sql NVARCHAR(MAX);

-- Função auxiliar: checar e adicionar coluna
CREATE TABLE #to_create (tbl SYSNAME, colname SYSNAME, coldef NVARCHAR(200));

INSERT INTO #to_create VALUES
('d_node','created_at','DATETIME2 NULL'),
('d_node','updated_at','DATETIME2 NULL'),
('d_node','user','VARCHAR(255) NULL'),
('d_interface','created_at','DATETIME2 NULL'),
('d_interface','updated_at','DATETIME2 NULL'),
('d_interface','user','VARCHAR(255) NULL'),
('d_custom_poller_assignment','created_at','DATETIME2 NULL'),
('d_custom_poller_assignment','updated_at','DATETIME2 NULL'),
('d_custom_poller_assignment','user','VARCHAR(255) NULL'),
('f_response_time','created_at','DATETIME2 NULL'),
('f_response_time','updated_at','DATETIME2 NULL'),
('f_response_time','user','VARCHAR(255) NULL'),
('f_custom_poller_statistics','created_at','DATETIME2 NULL'),
('f_custom_poller_statistics','updated_at','DATETIME2 NULL'),
('f_custom_poller_statistics','user','VARCHAR(255) NULL');

DECLARE cur CURSOR FOR SELECT tbl, colname, coldef FROM #to_create;
OPEN cur;
DECLARE @tbl SYSNAME, @col SYSNAME, @coldef NVARCHAR(200);
FETCH NEXT FROM cur INTO @tbl, @col, @coldef;
WHILE @@FETCH_STATUS = 0
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = @tbl AND COLUMN_NAME = @col
    )
    BEGIN
        SET @sql = N'ALTER TABLE dbo.' + QUOTENAME(@tbl) + ' ADD ' + QUOTENAME(@col) + ' ' + @coldef + ';';
        PRINT @sql;
        EXEC sp_executesql @sql;
    END
    ELSE
    BEGIN
        PRINT 'Column ' + @col + ' already exists on ' + @tbl + '; skipping.';
    END

    FETCH NEXT FROM cur INTO @tbl, @col, @coldef;
END

CLOSE cur;
DEALLOCATE cur;
DROP TABLE #to_create;

-- Fim do script

-- Remover coluna `date_time` e adicionar coluna `date` (DATE) nas tabelas de fato
-- Verifica existência antes de dropar/alterar para evitar erros

PRINT '--- Ajustando colunas de data nas tabelas de fato ---';

-- f_response_time: remover date_time e adicionar date (DATE)
IF EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'f_response_time' AND COLUMN_NAME = 'date_time'
)
BEGIN
    PRINT 'Dropping column date_time from f_response_time';
    ALTER TABLE dbo.f_response_time DROP COLUMN date_time;
END
ELSE
BEGIN
    PRINT 'Column date_time not found on f_response_time; skipping drop.';
END

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'f_response_time' AND COLUMN_NAME = 'date'
)
BEGIN
    PRINT 'Adding column date (DATE) to f_response_time';
    ALTER TABLE dbo.f_response_time ADD [date] DATE NULL;
END
ELSE
BEGIN
    PRINT 'Column date already exists on f_response_time; skipping add.';
END

-- f_custom_poller_statistics: remover date_time e adicionar date (DATE)
IF EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'f_custom_poller_statistics' AND COLUMN_NAME = 'date_time'
)
BEGIN
    PRINT 'Dropping column date_time from f_custom_poller_statistics';
    ALTER TABLE dbo.f_custom_poller_statistics DROP COLUMN date_time;
END
ELSE
BEGIN
    PRINT 'Column date_time not found on f_custom_poller_statistics; skipping drop.';
END

IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'f_custom_poller_statistics' AND COLUMN_NAME = 'date'
)
BEGIN
    PRINT 'Adding column date (DATE) to f_custom_poller_statistics';
    ALTER TABLE dbo.f_custom_poller_statistics ADD [date] DATE NULL;
END
ELSE
BEGIN
    PRINT 'Column date already exists on f_custom_poller_statistics; skipping add.';
END

PRINT '--- Ajuste de colunas de data finalizado ---';
