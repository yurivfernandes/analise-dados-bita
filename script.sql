SELECT *
FROM OPENQUERY(
    [172.21.3.221],     
    '
	SELECT
		Nodes.Nome_do_Cliente,
		Nodes.NodeID,
		Nodes.ID_VGR,
		Nodes.Caption,
		Nodes.Description,
		Nodes.Automatizacao,
		Nodes.Redundancia
    FROM [BR_TD_VITAIT].dbo.[Nodes] nodes
	WHERE nodes.Nome_do_cliente like ''%BRAD%''
	'
) AS Nodes

SELECT *
FROM OPENQUERY(
    [172.21.3.221],
    '
    SELECT 
        interfaces.NodeId,
        interfaces.InterfaceID,
        interfaces.InterfaceName,
        interfaces.Caption,
        interfaces.ID_VGR
    FROM [BR_TD_VITAIT].dbo.[Interfaces] interfaces
    INNER JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
        ON interfaces.NodeID = nodes.NodeID
    WHERE nodes.Nome_do_cliente LIKE ''%BRADESCO%''
    AND Tipo_Interface = ''WAN''
    '
) AS interfaces

SELECT *
FROM OPENQUERY(
    [172.21.3.221],     
    '
	SELECT 
		resp.NodeID,
		resp.DateTime,
		resp.AvgResponseTime,
		resp.PercentLoss
    FROM [BR_TD_VITAIT].dbo.[ResponseTime] resp
	LEFT JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
		ON resp.NodeID = nodes.NodeID
	WHERE nodes.Nome_do_cliente like ''%BRADESCO%''
	'
) AS ResponseTime

SELECT *
FROM OPENQUERY(
    [172.21.3.221],     
    '
	SELECT
		poller.CustomPollerAssignmentID,
		poller.NodeID
    FROM [BR_TD_VITAIT].dbo.[CustomPollerAssignment] poller
	LEFT JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
		ON poller.NodeID = nodes.NodeID
	WHERE nodes.Nome_do_cliente like ''%BRADESCO%''
	'
) AS CustomPollerAssignmentID
 
SELECT *
FROM OPENQUERY(
    [172.21.3.221],     
    '
	SELECT
		poller.CustomPollerAssignmentID,
		poller.NodeID,
		poller.RowID,
		poller.DateTime,
		poller.RawStatus,
		poller.Weight
    FROM [BR_TD_VITAIT].dbo.[CustomPollerStatistics_CS] poller
	LEFT JOIN [BR_TD_VITAIT].dbo.[CustomPollerAssignment] assignment
		on poller.CustomPollerAssignmentID = assignment.CustomPollerAssignmentID
	LEFT JOIN [BR_TD_VITAIT].dbo.[Nodes] nodes
		ON assignment.NodeID = nodes.NodeID
	WHERE nodes.Nome_do_cliente like ''%BRADESCO%''
	'
) AS CustomPollerStatistics_CS

