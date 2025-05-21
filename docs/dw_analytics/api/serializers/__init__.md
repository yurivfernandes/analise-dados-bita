# `__init__.py` da pasta serializers

## O que é?

O arquivo `__init__.py` transforma a pasta `serializers` em um módulo Python, permitindo importar serializers diretamente do pacote. Ele centraliza os imports dos serializers do app.

---

## Para que serve?

- Facilita o import dos serializers em outros arquivos (ex: views).
- Mantém o código organizado e evita importações circulares.
- Permite importar todos os serializers do app com uma única linha.

---

## Exemplo de código

```python
from .f_incidents_bita_serializer import FIncidentsBitaSerializer
```

- Importa o serializer do arquivo correspondente e o disponibiliza no pacote.
- Assim, em outros arquivos, pode-se importar diretamente:
  ```python
  from dw_analytics.api.serializers import FIncidentsBitaSerializer
  ```

---

## Funcionamento esperado

- Ao adicionar novos serializers, basta importar no `__init__.py` para que fiquem disponíveis no pacote.
- Mantém a estrutura do projeto limpa e organizada.

---

## O que pode e não pode alterar

- **Pode**: Adicionar/remover imports conforme novos serializers são criados ou removidos.
- **Não pode**: Remover o arquivo `__init__.py` se quiser manter a pasta como módulo Python.
