SELECT 
      
  cast([opened_at] as date)                  as 'aberto_em_data' 
 ,inc.opened_at
 ,inc.closed_at
 
 ,DATEDIFF(HOUR, opened_at, closed_at) AS horas
 ,CASE 
        WHEN DATEDIFF(HOUR, inc.opened_at, inc.closed_at) <= 24 THEN 'Aging até 24 horas'
        WHEN DATEDIFF(HOUR, inc.opened_at, inc.closed_at) <= 72 THEN 'Aging de 1 à 3 dias'
        WHEN DATEDIFF(HOUR, inc.opened_at, inc.closed_at) <= 168 THEN 'Aging de 4 à 7 dias'
        WHEN DATEDIFF(HOUR, inc.opened_at, inc.closed_at) <= 336 THEN 'Aging de 1 a 2 semanas'
        WHEN DATEDIFF(HOUR, inc.opened_at, inc.closed_at) <= 672 THEN 'Aging de 3 a 4 semanas'
        ELSE 'Aging acima de 1 mês'
    END AS aging_fechamento
   ,inc.[number]
   ,[dv_u_origem]                              as 'origem'
   ,company.nome_correto                       as 'company'
   ,grupo.dv_assignment_group                  as 'grupo_de_atribuicao'
   ,subCdetail.[dv_u_detail_subcategory]
   ,inc.contact_type                           as 'tipo_incident'
   ,[u_tipo_incidente]                         as 'tipo_incident_class'
   ,[dv_opened_by]                             as 'aberto_por'
   ,upper(fechado.dv_closed_by)                as 'fechado_por'
   ,[u_tipo_de_procedencia]                   as 'tipo de procedencia'
   ,[cmdb_ci]
   ,[u_designador]
   ,CASE 
      WHEN dv_priority IN ('1 - Critical', '1 - Crítica')   THEN '1 - Crítica'
      WHEN dv_priority IN ('2 - High', '2 - Alta')     THEN '2 - Alta'
      WHEN dv_priority IN ('3 - Moderate', '3 - Moderada')   THEN '3 - Moderada'
      WHEN dv_priority IN ('4 - Low', '4 - Baixa')     THEN '4 - Baixa'
      WHEN dv_priority IN ('5 - Planning', '5 - Planejamento')  THEN '5 - Planejamento'
    END             as 'prioridade'
   ,[short_description]                        as 'descricao_resumida'
   ,[short_description],
    LTRIM(RTRIM(
        RIGHT(
            [short_description],
            CASE 
                WHEN CHARINDEX('-', REVERSE([short_description])) > 0 
                THEN CHARINDEX('-', REVERSE([short_description])) - 1
                ELSE 0
            END
        )
    )) AS ultimo_texto
   ,[dv_state]                                 as 'status'
   ,falha.dv_u_categoria_da_falha              as 'categoria_falha_tecnologia'
   ,[close_code]                               as 'status_fechamento' 
   ,case when Len(inc.parent_incident) >1 then 'Filho' else 'Pai' end as 'parent'
   ,u_tempo_indisponivel
   ,case when len(u_tempo_indisponivel) >1 then 
  cast(replace(u_tempo_indisponivel,'1970-01-01','')  as time)  
   else null end as 'tmp_indisponivel_hhmmss'
   ,case when len(u_tempo_indisponivel) >1 then 
  CAST(DATEDIFF(DAY, '1970-01-01', u_tempo_indisponivel) AS BIGINT) * 86400 + DATEDIFF(SECOND, CAST(u_tempo_indisponivel AS DATE), u_tempo_indisponivel) 
    else null end AS 'tmp_indisponivel_second'
   ,sla.tmp_atendimento
   ,sla.tmp_Resolucao
   ,sla.SLA_Atendimento
   ,sla.[SLA Resolucao]
    ,case 
  when Len(inc.time_worked) < 1 then DATEDIFF(SECOND, opened_at, resolved_at)  
  else 
    DATEPART(HOUR, time_worked) * 3600 +
    DATEPART(MINUTE, time_worked) * 60 +
    DATEPART(SECOND, time_worked)
  end            as 'tmp_trabalho_second'
 ,case 
  when Len(inc.time_worked) < 1 then CONVERT(VARCHAR(8), DATEADD(SECOND, DATEDIFF(SECOND, opened_at, closed_at), 0), 108)  
  else 
    CAST(time_worked AS TIME)

  end            as 'tmp_trabalho_hhmmss'

     
  FROM [NID].[historico].[hist_servicenow_incident] as inc 
  left join [NID].[dimensao].[dim_servicenow_assignment_group] as grupo on grupo.id = inc.assignment_group
  left join [NID].[dimensao].[dim_servicenow_company] as company on company.company = inc.company
  left join [NID].[dimensao].[dim_servicenow_category] as category on category.category = inc.category
  left join [NID].[dimensao].[dim_servicenow_subcategory_detail] as subCdetail on subCdetail.[u_detail_subcategory] = inc.[u_detail_subcategory]
  left join [NID].[dimensao].[dim_servicenow_closed_by] as fechado on fechado.closed_by = inc.closed_by
  left join [NID].[dimensao].[dim_servicenow_categoria_da_falha] as falha on falha.u_categoria_da_falha = inc.u_categoria_da_falha
  left join [NID].[stage].[stg_servicenow_incident_sla] as sla on sla.[number] = inc.number
 
  where company.nome_correto like('%BRADESCO%') 
  
  ORDER BY 1 DESC 