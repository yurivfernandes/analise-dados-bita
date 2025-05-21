# `__init__.py` dos utilitários

## O que é?

O arquivo `__init__.py` transforma a pasta `utils` em um módulo Python, permitindo importar utilitários diretamente do pacote. Ele centraliza os imports das classes utilitárias do app.

---

## Para que serve?

- Facilita o import dos utilitários em outros arquivos (ex: views, tasks).
- Mantém o código organizado e evita importações circulares.
- Permite importar todos os utilitários do app com uma única linha.

---

## Exemplo de código

```python
from .pipeline import Pipeline
from .paginators import CustomPagination, CustomLargePagination
```

- Importa as classes utilitárias do arquivo correspondente e as disponibiliza no pacote.
- Assim, em outros arquivos, pode-se importar diretamente:
  ```python
  from app.utils import Pipeline, CustomPagination
  ```

---

## Funcionamento esperado

- Ao adicionar novos utilitários, basta importar no `__init__.py` para que fiquem disponíveis no pacote.
- Mantém a estrutura do projeto limpa e organizada.

---

## O que pode e não pode alterar

- **Pode**: Adicionar/remover imports conforme novos utilitários são criados ou removidos.
- **Não pode**: Remover o arquivo `__init__.py` se quiser manter a pasta como módulo Python.
