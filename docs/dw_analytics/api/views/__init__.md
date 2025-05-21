# `__init__.py` da pasta views

## O que é?

O arquivo `__init__.py` transforma a pasta `views` em um módulo Python, permitindo importar views diretamente do pacote. Ele também serve para centralizar e facilitar os imports das views do app.

---

## Para que serve?

- Permite importar todas as views do app de forma centralizada.
- Facilita o uso em arquivos de rotas (`urls.py`), evitando múltiplos imports espalhados.
- Ajuda a evitar problemas de importação circular.

---

## Exemplo de código

```python
from .f_incidents_bita_viewset import FIncidentsBitaViewset
```

- Este comando importa a classe `FIncidentsBitaViewset` do arquivo `f_incidents_bita_viewset.py` e a disponibiliza no pacote `views`.
- Assim, em outros arquivos, você pode importar diretamente:
  ```python
  from dw_analytics.api.views import FIncidentsBitaViewset
  ```

---

## Funcionamento esperado

- Ao adicionar novas views, basta importar no `__init__.py` para que fiquem disponíveis no pacote.
- Mantém o código limpo e organizado, especialmente em projetos grandes.

---

## O que pode e não pode alterar

- **Pode**: Adicionar/remover imports conforme novas views são criadas ou removidas.
- **Não pode**: Remover o arquivo `__init__.py` se quiser manter a pasta como módulo Python.
