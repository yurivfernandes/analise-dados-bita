# Pipeline Base

O pipeline define uma classe base para processamento de dados, padronizando logs de execução e facilitando o uso de context manager (`with`).

## Principais funcionalidades

- Log automático de inserções, deleções, início e fim do processamento.
- Cálculo automático de duração da execução.
- Uso de `with Pipeline() as p:` para garantir logs mesmo em caso de erro.

## Exemplo de uso

```python
from app.utils.pipeline import Pipeline

with Pipeline() as p:
    # processamento de dados
    pass
print(p.log)
```

# `pipeline.py`

## O que é?

Classe utilitária para padronizar o processamento de dados em pipelines, especialmente para ETL (Extract, Transform, Load) ou tarefas de carga de dados.

---

## Para que serve?

- Padronizar logs de execução de pipelines.
- Medir tempo de execução automaticamente.
- Facilitar o uso de context manager (`with`) para garantir logs mesmo em caso de erro.

---

## Código explicado

```python
from django.utils import timezone

class Pipeline:
    """Classe padrão que generaliza os métodos de todas as Pipelines de dados"""

    def __init__(self, **kwargs):
        self.log = {
            'n_inserted': 0,
            'n_deleted': 0,
            'started_at': timezone.now(),
            'finished_at': None,
            'duration': None
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log['finished_at'] = timezone.now()
        self.log['duration'] = (
            self.log['finished_at'] -
            self.log['started_at']).total_seconds()
```

### Linha a linha

- `__init__`: Inicializa o log da pipeline, marcando o início da execução e zerando contadores de inserção/remoção.
- `__enter__`: Permite o uso da classe com `with`, retornando a própria instância.
- `__exit__`: Ao sair do bloco `with`, registra o horário de término e calcula a duração total da execução.

---

## Como usar

```python
from app.utils.pipeline import Pipeline

with Pipeline() as p:
    # Seu processamento de dados aqui
    # Exemplo: p.log['n_inserted'] += 100
    pass

print(p.log)
# Saída esperada:
# {
#   'n_inserted': 100,
#   'n_deleted': 0,
#   'started_at': ...,
#   'finished_at': ...,
#   'duration': ...,
# }
```

---

## Funcionamento esperado

- O log é preenchido automaticamente com início, fim e duração.
- Você pode incrementar manualmente `n_inserted` e `n_deleted` conforme sua lógica.
- Mesmo em caso de erro, o tempo de execução será registrado.

---

## O que pode e não pode alterar

- **Pode**: Adicionar novos campos ao log, sobrescrever métodos para customizar comportamento.
- **Não pode**: Remover o uso de `__enter__` e `__exit__` se quiser manter o suporte ao context manager.

---
