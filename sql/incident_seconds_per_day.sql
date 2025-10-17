/*
 Consulta: segundos por dia que cada incidente ficou em aberto
 Fonte: dw_analytics.f_incident
 Saída: incident_number, day_date, seconds_open
 Observações:
  - Se a coluna closed_at for NULL, o script considera GETDATE() (momento atual).
  - Se quiser apenas duas colunas (incident_number, seconds_open) remova day_date
    do SELECT final ou agregue por dia conforme necessário.
  - Ajuste nomes de colunas/schema se sua tabela usar outros nomes.
*/

;WITH incidents AS (
    SELECT
        CAST([number] AS VARCHAR(100)) AS incident_number,
        opened_at,
        closed_at
    FROM dw_analytics.f_incident
    WHERE opened_at IS NOT NULL
),
date_expanded AS (
    -- primeiro dia de cada incidente
    SELECT
        incident_number,
        opened_at,
        closed_at,
        CAST(opened_at AS DATE) AS day_date
    FROM incidents
    UNION ALL
    -- dias seguintes até a data de fechamento (ou hoje se aberto)
    SELECT
        incident_number,
        opened_at,
        closed_at,
        DATEADD(DAY, 1, day_date)
    FROM date_expanded
    WHERE DATEADD(DAY, 1, day_date) <= CAST(ISNULL(closed_at, GETDATE()) AS DATE)
)
SELECT
    incident_number,
    day_date,
    -- segundos em que o incidente esteve aberto naquele dia
    DATEDIFF(SECOND,
        CASE WHEN opened_at > CAST(day_date AS DATETIME) THEN opened_at ELSE CAST(day_date AS DATETIME) END,
        CASE WHEN ISNULL(closed_at, GETDATE()) < DATEADD(DAY, 1, CAST(day_date AS DATETIME)) THEN ISNULL(closed_at, GETDATE()) ELSE DATEADD(DAY, 1, CAST(day_date AS DATETIME)) END
    ) AS seconds_open
FROM date_expanded
ORDER BY incident_number, day_date
OPTION (MAXRECURSION 0);
