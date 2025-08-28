SELECT
            *
FROM OPENQUERY(
    [172.21.3.221],
    '
		SELECT TOP(100)
	        traffic.NodeID,
			traffic.DateTime,
			traffic.In_Averagebps,
			traffic.Out_Averagebps
	    FROM [BR_TD_VITAIT].dbo.[InterfaceTraffic] traffic
		WHERE traffic.NodeID = ''310690''
') as nodes