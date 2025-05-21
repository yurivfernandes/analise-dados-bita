# Tasks do app power_bi

## O que são tasks?

Tasks são classes ou funções responsáveis por processar grandes volumes de dados, executar rotinas de ETL (Extract, Transform, Load), integrações ou cargas automatizadas. No contexto do Django, podem ser usadas em pipelines, comandos customizados ou integradas com Celery para execução assíncrona.

---

## Como funcionam as tasks no power_bi?

- Utilizam a classe base `Pipeline` para padronizar logs e execução.
- Podem ser usadas como context manager (`with`) para garantir logs mesmo em caso de erro.
- Executam extração, transformação e carga de dados entre diferentes modelos/tabelas.
- Podem ser chamadas por views, comandos de management ou agendadas via Celery.

---

## Exemplo de uso

```python
from power_bi.tasks import LoadInterfaceNewID

with LoadInterfaceNewID(company_remedy_list=[...], nome_do_cliente_list=[...]) as task:
    log = task.run()
print(log)
```

---

## Funcionamento esperado

- A task executa todas as etapas de ETL e retorna um log detalhado da execução.
- Pode ser facilmente integrada a endpoints de API ou rotinas agendadas.

---

Consulte os arquivos individuais para detalhes de cada task.
