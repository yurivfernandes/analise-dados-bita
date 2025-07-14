CREATE PROCEDURE dbo.CARGA_F_INCIDENTS_BITA
AS 

-- FAZ A CARGA DA TABELA f_incidents_bita NO BANCO POWER_BI NO SCHEMA dw_analytics.
-- ESSA TABELA SERVIRÁ PARA COMPOR O RELATÓRIO GERENCIAL DAS TAREFAS DA BITA

DELETE FROM f_incidents_bita

INSERT INTO f_incidents_bita
(
	number,
    resolved_at,
    u_origem,
    opened_at,
    assignment_group,
    opened_by,
    assigned_to,
    resolved_by,
    description,
    short_description,
    dv_state,
    close_notes,
    priority
)
SELECT 
    number,
    resolved_at,
    u_origem,
    opened_at,
    assignment_group,
    dv_opened_by as opened_by,
    dv_assigned_to as assigned_to,
    dv_resolved_by as resolved_by,
    description,
    short_description,
    dv_state,
    close_notes,
    priority
FROM 
    OPENQUERY(
        [172.21.1.5],
        '
        SELECT  
            number,
			assignment_group,
            resolved_at,
            u_origem,
			opened_at,
			dv_opened_by,
			dv_assigned_to,
			dv_resolved_by,
		    description,
		    short_description,
			dv_state,
			close_notes,
			priority
        FROM 
            [db_servicenow].dbo.incident AS incident  
        WHERE 
            incident.dv_assignment_group = ''BITA BI''
        '
    ) AS N