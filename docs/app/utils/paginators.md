# Paginadores Customizados

Este módulo pode conter classes para paginação customizada de querysets em APIs Django REST Framework.

## Possíveis funcionalidades

- Paginação baseada em número de página ou cursor.
- Customização de resposta (ex: incluir total de páginas, links de próxima/anterior página).
- Integração com filtros e ordenação.

> Consulte o código para detalhes de implementação e exemplos de uso.

# `paginators.py`

## O que é?

Arquivo que define paginadores customizados para APIs Django REST Framework. Paginadores são responsáveis por dividir grandes conjuntos de dados em páginas menores, facilitando o consumo por aplicações frontend.

---

## Para que serve?

- Controlar o tamanho das respostas das APIs.
- Permitir ao usuário navegar entre páginas de resultados.
- Customizar o formato da resposta paginada.

---

## Código explicado

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 1_000

    def get_paginated_response(self, data: dict) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "page_size": self.page_size,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )

class CustomLargePagination(CustomPagination):
    page_size = 1_000
    max_page_size = 10_000
```

### Linha a linha

- `CustomPagination` herda de `PageNumberPagination`, o paginador padrão do DRF.
- `page_size = 50`: Define o tamanho padrão da página.
- `page_size_query_param = "page_size"`: Permite ao usuário definir o tamanho da página via query string (`?page_size=100`).
- `max_page_size = 1_000`: Limita o tamanho máximo da página.
- `get_paginated_response`: Customiza a resposta, incluindo:
  - `count`: total de itens.
  - `page_size`: tamanho da página.
  - `next`/`previous`: links para próxima/anterior página.
  - `total_pages`: número total de páginas.
  - `results`: os dados da página atual.

- `CustomLargePagination` herda de `CustomPagination` e aumenta os limites para grandes volumes de dados.

---

## Como usar

No seu `settings.py`:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "app.utils.paginators.CustomPagination",
    "PAGE_SIZE": 50,
    # ...
}
```

Ou diretamente em uma view DRF:

```python
from app.utils.paginators import CustomPagination

class MinhaViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
```

---

## Funcionamento esperado

- Ao acessar uma rota paginada, a resposta será um JSON com os campos definidos em `get_paginated_response`.
- O usuário pode navegar entre páginas usando os links `next` e `previous` e ajustar o tamanho da página via `page_size`.

---

## O que pode e não pode alterar

- **Pode**: Customizar os campos retornados, alterar limites de página, criar novos paginadores herdando de `CustomPagination`.
- **Não pode**: Remover métodos essenciais ou alterar a assinatura de `get_paginated_response` sem entender o impacto.

---
