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
	CASE 
	    WHEN ISDATE(inc.opened_at) = 1 THEN CAST(inc.opened_at AS DATE)
	    ELSE NULL
	END AS 'Data Abertura',
	CASE 
	    WHEN ISDATE(inc.closed_at) = 1 THEN CAST(inc.closed_at AS DATE)
	    ELSE NULL
	END AS 'Data Fechamento',
	CASE 
	    WHEN ISDATE(inc.closed_at) = 1 THEN CAST(inc.closed_at AS DATE)
	    ELSE NULL
	END AS 'Data Fim da indisponibilidade',
    --inc.parent_incident AS 'Incidente Pai',
    UPPER(inc.category) AS 'Categoria de Abertura',
    UPPER(inc.subcategory) AS 'Subcategoria de Abertura',
    UPPER(inc.u_detail_subcategory) AS 'Detalhe Subcategoria de Abertura',
    UPPER(inc.u_categoria_da_falha) AS 'Categoria da Falha',
    UPPER(inc.u_sub_categoria_da_falha) AS 'Subcategoria da Falha',
    UPPER(inc.u_detalhe_sub_categoria_da_falha) AS 'Detalhe Subcategoria da Faha',
    inc.short_description AS 'Título do Chamado',
    ISNULL(UPPER(inc.contact_type),'OUTROS') AS 'Tipo do contato',    
    inc.cmdb_ci AS 'CMDB ID',
    UPPER(inc.state) AS 'Status',
    UPPER(inc.u_origem) AS 'Origem',
    
    --CAMPOS DE FILA--
    UPPER(assignment_group.name) AS 'Torre de atendimento',
    
    --CAMPOS DE SLA
    sla_first.sla_atendimento AS 'SLA Atendimento',
    sla_resolved.sla_resolucao as 'SLA Resolução',
    sla_first.business_duration AS 'Duração SLA Atendimento (segundos)',
    sla_resolved.business_duration AS 'Duração SLA Resolução (segundos)',
    
    --CAMPOS DO CLIENTE
    ISNULL(company_name.nome_correto, company.name) AS 'Cliente',
    
    --CAMPOS DO CONTRATO
    contract.number AS 'Número do Contrato',

    -- CAMPOS CALCULADOS --
    
    ----- [SOMENTE BRADESCO] CAMPO LOCALIDADE -----
    CASE
	    WHEN (LEFT(CAST(inc.short_description AS varchar(8000)), 5) = '[BRAD'
	          OR LEFT(CAST(inc.short_description AS varchar(8000)), 4) = 'BRAD')
	         AND CHARINDEX('_', CAST(inc.short_description AS varchar(8000))) > 1
	    THEN SUBSTRING(
	        CAST(inc.short_description AS varchar(8000)),
	        CASE 
	            WHEN LEFT(CAST(inc.short_description AS varchar(8000)), 5) = '[BRAD' THEN 2
	            ELSE 1
	        END,
	        CHARINDEX('_', CAST(inc.short_description AS varchar(8000))) - 
	        CASE 
	            WHEN LEFT(CAST(inc.short_description AS varchar(8000)), 5) = '[BRAD' THEN 2
	            ELSE 1
	        END
	    )
	    ELSE NULL
	END AS Localidade,
    ----- [SOMENTE BRADESCO] CAMPO LOCALIDADE ----
    
    ----- TEMPO INDISPONÍVEL EM SEGUNDOS -----
    CASE 
    	WHEN inc.contact_type = 'ALERT'
    	THEN 'PROATIVO'
    	ELSE 'REATIVO'
    END AS 'Tipo abertura',

    CASE 
    	WHEN inc.parent_incident IS NULL
    	THEN 'PAI'
    	ELSE 'FILHO'
    END AS 'Incidente Pai ou Filho',
    
    CASE 
        WHEN CHARINDEX('Day', inc.u_tempo_indisponivel) > 0 THEN
            TRY_CAST(SUBSTRING(inc.u_tempo_indisponivel, 
                CHARINDEX('Day', inc.u_tempo_indisponivel) - 3, 3) AS INT)
        ELSE 0
    END * 86400 +
    CASE 
        WHEN CHARINDEX('Hour', inc.u_tempo_indisponivel) > 0 THEN
            TRY_CAST(SUBSTRING(inc.u_tempo_indisponivel, 
                CHARINDEX('Hour', inc.u_tempo_indisponivel) - 3, 3) AS INT)
        ELSE 0
    END * 3600 +
    CASE 
        WHEN CHARINDEX('Minute', inc.u_tempo_indisponivel) > 0 THEN
            TRY_CAST(SUBSTRING(inc.u_tempo_indisponivel, 
                CHARINDEX('Minute', inc.u_tempo_indisponivel) - 3, 3) AS INT)
        ELSE 0
    END * 60 +
    CASE 
        WHEN CHARINDEX('Second', inc.u_tempo_indisponivel) > 0 THEN
            TRY_CAST(SUBSTRING(inc.u_tempo_indisponivel, 
                CHARINDEX('Second', inc.u_tempo_indisponivel) - 3, 3) AS INT)
        ELSE 0
    END AS 'Tempo Indisponível (segundos)',
	
    ----- HORAS TRABALHADAS EM SEGUNDOS -----
    CASE 
        WHEN CHARINDEX('Day', inc.time_worked) > 0 THEN
            TRY_CAST(SUBSTRING(inc.time_worked, 
                CHARINDEX('Day', inc.time_worked) - 3, 3) AS INT)
        ELSE 0
    END * 86400 +
    CASE 
        WHEN CHARINDEX('Hour', inc.time_worked) > 0 THEN
            TRY_CAST(SUBSTRING(inc.time_worked, 
                CHARINDEX('Hour', inc.time_worked) - 3, 3) AS INT)
        ELSE 0
    END * 3600 +
    CASE 
        WHEN CHARINDEX('Minute', inc.time_worked) > 0 THEN
            TRY_CAST(SUBSTRING(inc.time_worked, 
                CHARINDEX('Minute', inc.time_worked) - 3, 3) AS INT)
        ELSE 0
    END * 60 +
    CASE 
        WHEN CHARINDEX('Second', inc.time_worked) > 0 THEN
            TRY_CAST(SUBSTRING(inc.time_worked, 
                CHARINDEX('Second', inc.time_worked) - 3, 3) AS INT)
        ELSE 0
    END AS 'Horas Trabalhadas (segundos)',
    ----- HORAS TRABALHADAS EM SEGUNDOS -----

	----- CORREÇÃO DO CAMPO PRIORIDADE/CRITICIDADE -----
    CASE 
        WHEN priority IN ('1','1 - Critical', '1 - Crítica')   THEN '1 - Crítica'
        WHEN priority IN ('2','2 - High', '2 - Alta')           THEN '2 - Alta'
        WHEN priority IN ('3','3 - Moderate', '3 - Moderada')   THEN '3 - Moderada'
        WHEN priority IN ('4','4 - Low', '4 - Baixa')           THEN '4 - Baixa'
        WHEN priority IN ('5','5 - Planning', '5 - Planejamento') THEN '5 - Planejamento'
    END AS 'Prioridade'
    
    ----- CORREÇÃO DO CAMPO PRIORIDADE/CRITICIDADE -----

FROM incident inc 

-- JOINS COM AS TABELAS DIMENÇÕES --
LEFT JOIN sys_company company
    ON inc.company = company.sys_id
LEFT JOIN company_name_mapping company_name
  ON company.name LIKE '%' + company_name.dv_company + '%'
LEFT JOIN groups assignment_group
	ON inc.assignment_group = assignment_group.sys_id
LEFT JOIN ast_contract contract
	ON inc.contract = contract.sys_id
LEFT JOIN sla_first
	ON inc.sys_id = sla_first.task
LEFT JOIN sla_resolved
    ON inc.sys_id = sla_resolved.task
LEFT JOIN book_cliente book_cliente
    ON ISNULL(company_name.nome_correto, company.name) = book_cliente.cliente_nome
    
-- FILTROS DO RELATÓRIO PADRÃO --
WHERE book_cliente.origem = 'VGR'
and ISNULL(company_name.nome_correto, company.name) LIKE '%SUZANO%';
