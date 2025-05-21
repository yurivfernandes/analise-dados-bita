# `f_incidents_bita_viewset.py`

## O que é?

Arquivo que define o viewset responsável por expor a API para o modelo `FIncidentsBita` do app **dw_analytics**.

---

## Código explicado ponto a ponto

```python
from rest_framework.viewsets import ModelViewSet
```
- Importa o `ModelViewSet` do Django REST Framework, que já implementa todas as operações CRUD (listar, criar, atualizar, deletar).

```python
from app.utils.paginators import CustomLargePagination
```
- Importa um paginador customizado, que define o tamanho das páginas e o formato da resposta paginada.

```python
from ...models import FIncidentsBita
from ..serializers import FIncidentsBitaSerializer
```
- Importa o modelo `FIncidentsBita` (representa a tabela no banco de dados).
- Importa o serializer, responsável por converter o modelo em JSON para a API.

```python
class FIncidentsBitaViewset(ModelViewSet):
    serializer_class = FIncidentsBitaSerializer
    queryset = FIncidentsBita.objects.using("dw_analytics").all()
    pagination_class = CustomLargePagination
```
- Define a classe `FIncidentsBitaViewset`, herdando de `ModelViewSet`.
- `serializer_class`: Indica qual serializer será usado para transformar os dados.
- `queryset`: Define o conjunto de dados que será exposto pela API. O método `.using("dw_analytics")` garante que a consulta será feita no banco correto.
- `pagination_class`: Define o paginador a ser usado para as respostas dessa view.

---

## Funcionamento esperado

- A view expõe endpoints RESTful para listar, criar, atualizar e deletar registros de `FIncidentsBita`.
- As respostas são paginadas conforme definido em `CustomLargePagination`.
- O serializer garante que os dados estejam no formato correto para a API.

---

## O que pode e não pode alterar

- **Pode**: Customizar o queryset, trocar o serializer, alterar o paginador, sobrescrever métodos para lógica customizada.
- **Não pode**: Remover a herança de `ModelViewSet` se quiser manter as operações CRUD automáticas.
