# Utilitários do App

Esta pasta contém utilitários reutilizáveis para o projeto, como pipelines de processamento de dados e paginadores customizados.

## Submódulos

- [`pipeline.md`](./pipeline.md): Pipeline base para processamento de dados.
- [`paginators.md`](./paginators.md): Paginadores customizados para APIs.

Consulte cada arquivo para detalhes de implementação e exemplos de uso.

---

## Como importar utilitários

O arquivo `__init__.py` importa as classes utilitárias principais, facilitando o uso em outros módulos:

```python
from .pipeline import Pipeline
from .paginators import CustomPagination, CustomLargePagination
```

Assim, basta importar diretamente:

```python
from app.utils import Pipeline, CustomPagination
```
