WITH sla_first AS (
    SELECT *
    FROM (
        SELECT 
            sla.task AS task,
            CAST(DATEDIFF(SECOND, '1970-01-01 00:00:00', sla.business_duration) AS FLOAT) AS business_duration,
            sla.has_breached AS sla_atendimento,
            contract_sla.sys_name AS nome_sla,
            ROW_NUMBER() OVER (PARTITION BY sla.task ORDER BY sla.sys_created_on DESC) AS rn
        FROM incident_sla sla
        LEFT JOIN contract_sla contract_sla ON sla.sla = contract_sla.sys_id
        WHERE contract_sla.sys_name LIKE '%VGR] SLA Atendimento%'
    ) AS sub
    WHERE rn = 1
),
sla_resolved AS (
    SELECT *
    FROM (
        SELECT 
            sla.task AS task,
            CAST(DATEDIFF(SECOND, '1970-01-01 00:00:00', sla.business_duration) AS FLOAT) AS business_duration,
            sla.has_breached AS sla_resolucao,
            contract_sla.sys_name AS nome_sla,
            ROW_NUMBER() OVER (PARTITION BY sla.task ORDER BY sla.sys_created_on DESC) AS rn
        FROM incident_sla sla
        LEFT JOIN contract_sla contract_sla ON sla.sla = contract_sla.sys_id
        WHERE contract_sla.sys_name LIKE '%VGR] SLA Resolução%'
    ) AS sub
    WHERE rn = 1
)

SELECT TOP(100)
	--CAMPOS DO INCIDENTE--
	inc.sys_id AS 'ID',
    inc.number AS 'Incidente',
    --CAMPOS DE SLA
    sla_first.sla_atendimento AS 'SLA Atendimento',
    sla_resolved.sla_resolucao as 'SLA Resolução',
    sla_first.business_duration AS 'Duração SLA Atendimento (segundos)',
    sla_resolved.business_duration AS 'Duração SLA Resolução (segundos)'

FROM incident inc 

-- JOINS COM AS TABELAS DIMENÇÕES --
LEFT JOIN sys_company company
    ON inc.company = company.sys_id
LEFT JOIN company_name_mapping company_name
	ON company.name = company_name.dv_company
LEFT JOIN sla_first
	ON inc.sys_id = sla_first.task
LEFT JOIN sla_resolved
    ON inc.sys_id = sla_resolved.task
LEFT JOIN book_cliente book_cliente
    ON ISNULL(company_name.nome_correto, company.name) = book_cliente.cliente_nome
    
-- FILTROS DO RELATÓRIO PADRÃO --
WHERE book_cliente.origem = 'VGR';
