-- create_task_log.sql
-- Script para criar a tabela dbo.task_log no SQL Server
-- Garante que a tabela exista, adiciona constraint para validar JSON e índice em run_at

IF OBJECT_ID('dbo.task_log', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.task_log (
        id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        task_name NVARCHAR(255) NOT NULL,
        run_at DATETIME2 NOT NULL,
        -- Armazenamos o JSON em NVARCHAR(MAX) e garantimos validade JSON com ISJSON
        log NVARCHAR(MAX) NOT NULL,
        CONSTRAINT CK_task_log_log_is_json CHECK (ISJSON(log) = 1)
    );

    -- Índice em run_at para consultas por data
    CREATE INDEX IX_task_log_run_at ON dbo.task_log(run_at);
END
ELSE
BEGIN
    PRINT 'A tabela dbo.task_log já existe.';
END

-- Exemplo de INSERT para teste
-- Substitua os valores conforme necessário
-- INSERT INTO dbo.task_log (task_name, run_at, log)
-- VALUES (
--     'LoadResponseTime',
--     SYSUTCDATETIME(), -- ou GETDATE() / SYSDATETIME()
--     N'{"start_time":"2025-08-25T10:00:00Z","end_time":"2025-08-25T10:05:30Z","duration_seconds":330.0}'
-- );

-- Observações:
-- 1) Este script cria apenas a tabela; os campos `start_time`/`end_time`/`duration` mencionados
--    nos logs devem ser gerados e persistidos pela sua aplicação dentro do JSON armazenado
--    na coluna `log` (TaskLog.log).
-- 2) Se desejar colunas separadas (e.g. start_time DATETIME2, end_time DATETIME2, duration_seconds FLOAT),
--    posso gerar uma versão do script com essas colunas e índices apropriados.
