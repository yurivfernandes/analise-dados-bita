CREATE PROC [dbo].[ETL_INCIDENTES_SERVICE_NOW]
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Variável para controle de atualização incremental
    DECLARE @data_corte DATETIME = DATEADD(DAY, -10, GETDATE());
    
    -- Inserir novos Assignment Groups
    MERGE INTO d_assignment_group AS target
    USING (
        SELECT DISTINCT 
            LTRIM(RTRIM(inc.assignment_group)) AS id,
            MAX(LTRIM(RTRIM(inc.dv_assignment_group)) ) AS dv_assignment_group
        FROM SERVICE_NOW.dbo.incident inc
        WHERE inc.assignment_group IS NOT NULL
            AND inc.assignment_group != ''
            AND inc.dv_assignment_group IS NOT NULL
            AND inc.dv_assignment_group != ''
            AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte)
        GROUP BY inc.assignment_group
    ) AS source
    ON target.id = source.id
    
    WHEN MATCHED THEN
        UPDATE SET target.dv_assignment_group = source.dv_assignment_group
    
    WHEN NOT MATCHED THEN
        INSERT (id, dv_assignment_group)
        VALUES (source.id, source.dv_assignment_group);

    -- Inserir novos Resolved By
    --DELETE from d_resolved_by_assignment_group 
    DELETE FROM d_resolved_by 
          
    INSERT INTO d_resolved_by (id, dv_resolved_by)
    SELECT DISTINCT
        inc.resolved_by AS id,
        (SELECT TOP 1 inc2.dv_resolved_by
         FROM SERVICE_NOW.dbo.incident inc2
         WHERE inc2.resolved_by = inc.resolved_by
         ORDER BY inc2.sys_updated_on DESC) AS dv_resolved_by
    FROM SERVICE_NOW.dbo.incident inc
    WHERE inc.resolved_by IS NOT NULL
        AND inc.resolved_by != ''
        AND inc.dv_resolved_by != ''
   
    -- Relacionamento Resolved By - Assignment Group
--    INSERT INTO d_resolved_by_assignment_group (resolved_by_id, assignment_group_id)
--    SELECT resolved_by_id, assignment_group_id
--    FROM (
--        SELECT 
--            LTRIM(RTRIM(inc.resolved_by)) AS resolved_by_id,
--            LTRIM(RTRIM(inc.assignment_group)) AS assignment_group_id,
--            ROW_NUMBER() OVER (PARTITION BY LTRIM(RTRIM(inc.resolved_by)), LTRIM(RTRIM(inc.assignment_group)) ORDER BY (SELECT NULL)) AS rn
--        FROM SERVICE_NOW.dbo.incident inc
--        INNER JOIN d_resolved_by rb 
--            ON LTRIM(RTRIM(inc.resolved_by)) = rb.id
--        INNER JOIN d_assignment_group ag 
--            ON LTRIM(RTRIM(inc.assignment_group)) = ag.id
--        WHERE inc.resolved_by IS NOT NULL
--        AND inc.assignment_group IS NOT NULL
--        AND inc.resolved_by != ''
--        AND inc.assignment_group != ''
--          --AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte)
--    ) AS SubQuery
--    WHERE rn = 1;
    
    DELETE FROM d_contract
    -- Inserir novos Contracts
    INSERT INTO d_contract (id, dv_contract)
    SELECT DISTINCT
        LTRIM(RTRIM(inc.contract)) AS id,
        LTRIM(RTRIM(inc.dv_contract)) AS dv_contract
    FROM SERVICE_NOW.dbo.incident inc
    LEFT JOIN d_contract c 
        ON LTRIM(RTRIM(inc.contract)) = c.id
    WHERE c.id IS NULL
        AND inc.contract IS NOT NULL
        AND inc.contract != ''
        AND inc.dv_contract != ''
        AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte);
    
    --DELETE FROM d_company
    -- Inserir novas Companies
    WITH LatestCompany AS (
    SELECT 
            LTRIM(RTRIM(inc.company)) AS id,
            LTRIM(RTRIM(inc.dv_company)) AS dv_company,
            REPLACE(REPLACE(REPLACE(LTRIM(RTRIM(inc.u_cnpj)), '.', ''), '/', ''), '-', '') AS u_cnpj,
            ROW_NUMBER() OVER (PARTITION BY inc.company ORDER BY inc.opened_at DESC) AS rn
        FROM SERVICE_NOW.dbo.incident inc
        WHERE inc.company IS NOT NULL
            AND inc.company != ''
            AND inc.dv_company != ''
            AND inc.u_cnpj != ''
            AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte)
    )
    MERGE INTO d_company AS target
    USING (SELECT id, dv_company, u_cnpj FROM LatestCompany WHERE rn = 1) AS source
    ON target.id = source.id
    WHEN MATCHED THEN
        UPDATE SET target.dv_company = source.dv_company, target.u_cnpj = source.u_cnpj
    WHEN NOT MATCHED THEN
        INSERT (id, dv_company, u_cnpj) VALUES (source.id, source.dv_company, source.u_cnpj);


    -- Apagar incidentes abertos e fechados nos últimos 10 dias
   DELETE FROM f_incident
   WHERE opened_at >= @data_corte OR closed_at >= @data_corte;

     -- Inserir ou atualizar Incidents na tabela fato
    MERGE f_incident AS target
    USING (
   SELECT 
            number, resolved_by, assignment_group, opened_at, closed_at,
            contract, dv_sla_first,dv_sla_resolved, sla_atendimento, sla_resolucao, company,
         u_origem, dv_u_categoria_da_falha, dv_u_sub_categoria_da_falha,
            dv_u_detalhe_sub_categoria_da_falha, dv_state,u_id_vgr, u_id_vantive,
            dv_category,dv_subcategory,dv_u_detail_subcategory, u_tipo_indisponibilidade,
            sys_id,resolved_at,scr_vendor_ticket, u_tipo_de_procedencia, u_data_normalizacao_servico,
            u_vendor_ticket,u_justificativa_isolamento,u_tempo_indisponivel,
            parent_incident,short_description,dv_location,description
        FROM (
            SELECT 
                inc.number,
                inc.resolved_by,
                inc.assignment_group,
                inc.opened_at,
                inc.closed_at,
                inc.contract,
                sla_first.has_breached as sla_atendimento,
                sla_resolved.has_breached as sla_resolucao,
                sla_first.dv_sla as dv_sla_first,
                sla_resolved.dv_sla as dv_sla_resolved,
                inc.company,
                inc.u_origem,
                inc.dv_u_categoria_da_falha,
                inc.dv_u_sub_categoria_da_falha,
                inc.dv_u_detalhe_sub_categoria_da_falha,
                inc.dv_state,
                inc.u_id_vgr,
                inc.u_id_vantive,
                inc.dv_category,
                inc.dv_subcategory,
                inc.dv_u_detail_subcategory,
                inc.u_tipo_indisponibilidade,
                inc.sys_id,
                inc.resolved_at,
                inc.scr_vendor_ticket,
                inc.u_tipo_de_procedencia,
                inc.u_data_normalizacao_servico,
                inc.u_vendor_ticket,
                inc.u_justificativa_isolamento,
                inc.u_tempo_indisponivel,
                inc.parent_incident,
                inc.short_description,
                inc.dv_location,
                inc.description,
                ROW_NUMBER() OVER (
                    PARTITION BY inc.number 
                    ORDER BY 
                        CASE 
                            WHEN inc.dv_state IN ('Encerrado', 'Closed') THEN 0
                            ELSE 1
                        END,
                        inc.sys_id
                ) as rn
            FROM SERVICE_NOW.dbo.incident inc
            LEFT JOIN SERVICE_NOW.dbo.incident_sla sla_first 
                ON inc.sys_id = sla_first.task 
                AND (
                sla_first.dv_sla LIKE '%VITA] FIRST%' 
                or sla_first.dv_sla LIKE '%VGR] SLA Atendimento%'
                )
            LEFT JOIN SERVICE_NOW.dbo.incident_sla sla_resolved 
                ON inc.sys_id = sla_resolved.task 
                AND (
                sla_resolved.dv_sla LIKE '%VITA] RESOLVED%' 
                or sla_resolved.dv_sla LIKE '%VGR] SLA Resolução%'
                )

            WHERE inc.number IS NOT NULL
            and (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte)
        ) AS DedupedIncidents
        WHERE rn = 1
    ) AS source
    ON target.number = source.number
    WHEN MATCHED THEN
        UPDATE SET
            resolved_by = source.resolved_by,
            assignment_group = source.assignment_group,
            opened_at = source.opened_at,
            closed_at = source.closed_at,
            contract = source.contract,
            dv_sla_first = source.dv_sla_first,
            dv_sla_resolved = source.dv_sla_resolved,
            sla_atendimento = source.sla_atendimento,
            sla_resolucao = source.sla_resolucao,
            company = source.company,
            u_origem = source.u_origem,
    		dv_u_categoria_da_falha = source.dv_u_categoria_da_falha,
            dv_u_sub_categoria_da_falha = source.dv_u_sub_categoria_da_falha,
            dv_u_detalhe_sub_categoria_da_falha = source.dv_u_detalhe_sub_categoria_da_falha,
            dv_state = SOURCE.dv_state,
            u_id_vgr = SOURCE.u_id_vgr,
            u_id_vantive=SOURCE.u_id_vantive,
            dv_category=SOURCE.dv_category,
            dv_subcategory=SOURCE.dv_subcategory,
            dv_u_detail_subcategory=SOURCE.dv_u_detail_subcategory,
            u_tipo_indisponibilidade=SOURCE.u_tipo_indisponibilidade,
            sys_id = SOURCE.sys_id,
            resolved_at = SOURCE.resolved_at,
            scr_vendor_ticket = SOURCE.scr_vendor_ticket,
            u_tipo_de_procedencia = SOURCE.u_tipo_de_procedencia,
            u_data_normalizacao_servico = SOURCE.u_data_normalizacao_servico,
            u_vendor_ticket = SOURCE.u_vendor_ticket,
            u_justificativa_isolamento = SOURCE.u_justificativa_isolamento, 
            u_tempo_indisponivel = SOURCE.u_tempo_indisponivel,
            parent_incident= SOURCE.parent_incident,
            short_description = SOURCE.short_description,
            dv_location = SOURCE.dv_location,
            description = SOURCE.description
    WHEN NOT MATCHED THEN
        INSERT (
            number, resolved_by, assignment_group, opened_at, closed_at,
  contract, dv_sla_first,dv_sla_resolved, sla_atendimento, sla_resolucao, company,
          u_origem, dv_u_categoria_da_falha, dv_u_sub_categoria_da_falha,
            dv_u_detalhe_sub_categoria_da_falha, dv_state, u_id_vgr,u_id_vantive,
            dv_category,dv_subcategory,dv_u_detail_subcategory,u_tipo_indisponibilidade,
         sys_id,resolved_at, scr_vendor_ticket, u_tipo_de_procedencia,u_data_normalizacao_servico,
         u_vendor_ticket,u_justificativa_isolamento,u_tempo_indisponivel,
         parent_incident,short_description,dv_location,description
        )
        VALUES (
            source.number, source.resolved_by, source.assignment_group,
            source.opened_at, source.closed_at, source.contract,
            source.dv_sla_first, source.dv_sla_resolved, 
            source.sla_atendimento, source.sla_resolucao, source.company,
            source.u_origem, source.dv_u_categoria_da_falha,
            source.dv_u_sub_categoria_da_falha,
            source.dv_u_detalhe_sub_categoria_da_falha,
            source.dv_state,source.u_id_vgr,source.u_id_vantive,
            source.dv_category,source.dv_subcategory,source.dv_u_detail_subcategory,
            source.u_tipo_indisponibilidade,source.sys_id, source.resolved_at,
            source.scr_vendor_ticket,u_tipo_de_procedencia,
            source.u_data_normalizacao_servico,
            source.u_vendor_ticket,
            source.u_justificativa_isolamento,
            source.u_tempo_indisponivel,
            source.parent_incident,
            source.short_description,
            source.dv_location,
            source.description
        );

       
----CARREGA A d_incident_sla COM OS SLAS DOS CHAMADOS QUE NÃO SÃO DA ORIGEM VGR
       
DELETE FROM d_incident_sla
WHERE EXISTS (
    SELECT 1
    FROM SERVICE_NOW.dbo.incident inc
    WHERE d_incident_sla.ticket = inc.number
    AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte)
   );

DECLARE @max_id INT;

-- Obtendo o último ID registrado
SELECT @max_id = ISNULL(MAX(id), 0) FROM d_incident_sla;

-- Inserindo com IDs incrementados manualmente
INSERT INTO d_incident_sla (id, ticket, nome, status)
SELECT  
    @max_id + ROW_NUMBER() OVER (ORDER BY inc.number) AS id,
    inc.number AS ticket,
    sla.dv_sla AS nome,
    CASE 
        WHEN sla.has_breached = 0 THEN 'DENTRO'
        WHEN sla.has_breached = 1 THEN 'FORA'
        ELSE '-'  
    END AS status
FROM SERVICE_NOW.dbo.incident_sla AS sla
LEFT JOIN SERVICE_NOW.dbo.incident AS inc ON sla.task = inc.sys_id 
WHERE  
    sla.dv_sla <> ''
    AND inc.u_origem NOT LIKE '%vgr%'
    AND (inc.opened_at >= @data_corte OR inc.closed_at >= @data_corte);   

---***ATUALIZA OS ULTIMOS 10 DIAS DA TABELA DE LOCALIDADES DO SAE


---- ATUALIZADA TABELE DE ACIONAMENTOS SERVICENOW
DELETE FROM f_incident_task 
WHERE u_data_in_cio  >= @data_corte OR u_data_fim >= @data_corte;

insert into f_incident_task 
SELECT DISTINCT
  incident
 ,u_operadora_integrador
 ,u_outros
 ,u_designa_o_lp 
 ,u_protocolo 
 ,u_data_in_cio
 ,u_data_fim
 ,u_tipo_acionamento
 ,u_produto
 ,description
FROM service_now.dbo.incident_task
WHERE u_data_in_cio  >= @data_corte OR u_data_fim >= @data_corte;

---*** ATUALIZA PLANTA ATIVA DOS CLIENTES VGR

DELETE FROM f_planta_vgr

INSERT INTO f_planta_vgr
SELECT
*
FROM 
    OPENQUERY([10.128.223.125],
    'SELECT
         [ID_VANTIVE]
        ,[RAIZ_COD_CLI]
        ,[COD_GRUPO]
        ,[CLIENTE]
        ,[GRUPO_ECONOMICO]
        ,[CNPJ]
        ,[STATUS_VANTIVE]
        ,[SERVICO]
        ,[ENDERECO_COMPLETO]
        ,[CIDADE]
        ,[UF]
        ,[CEP]
        ,[REGIONAL]
        ,[DATA_CONTRATO]
        ,[DATA_ENTRADA]
        ,[DATA_RFS]
        ,[DATA_RFB]
        ,[DATA_RFB_NAO_FATURAVEL]
        ,[DATA_CANCELAMENTO]
        ,[ISIS_CANCELAMENTO_MOTIVO]
        ,[JUSTIF_RFB]
        ,[ISIS_MOTIVO_PENDENCIA]
        ,[COMBO]
        ,[CAIXA_UNICA]
        ,[REVENDA_VGR]
        ,[MODELO_ATRIBUTOS]
        ,[PROJETO_ESPECIAL]
        ,[DELTA_REC_LIQ]
    FROM 
        LK_RELATORIO_12.SAE.SAE.TB_PEDIDOS_DADOS with (nolock)
    WHERE
        SERVICO = ''VIVO GESTÃO DE REDES''
        AND
        (
        CLIENTE NOT LIKE ''TELEFONICA%''
        )
')
END;