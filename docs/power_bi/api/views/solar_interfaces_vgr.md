# `solar_interfaces_vgr.py`

## O que é?

Arquivo que define o viewset responsável por expor a API para o modelo `TblSolarInterfacesVgr` do app **power_bi**.

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
from ...models import TblSolarInterfacesVgr
from ..serializers import SolarInterfacesVgrSerializer
```
- Importa o modelo `TblSolarInterfacesVgr` (representa a tabela no banco de dados).
- Importa o serializer, responsável por converter o modelo em JSON para a API.

```python
class SolarInterfacesVGR(ModelViewSet):
    serializer_class = SolarInterfacesVgrSerializer
    queryset = TblSolarInterfacesVgr.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
```
- Define a classe `SolarInterfacesVGR`, herdando de `ModelViewSet`.
- `serializer_class`: Indica qual serializer será usado para transformar os dados.
- `queryset`: Define o conjunto de dados que será exposto pela API. O método `.using("power_bi")` garante que a consulta será feita no banco correto.
- `pagination_class`: Define o paginador a ser usado para as respostas dessa view.

---

## Funcionamento esperado

- A view expõe endpoints RESTful para listar, criar, atualizar e deletar registros de `TblSolarInterfacesVgr`.
- As respostas são paginadas conforme definido em `CustomLargePagination`.
- O serializer garante que os dados estejam no formato correto para a API.

---

## O que pode e não pode alterar

- **Pode**: Customizar o queryset, trocar o serializer, alterar o paginador, sobrescrever métodos para lógica customizada.
- **Não pode**: Remover a herança de `ModelViewSet` se quiser manter as operações CRUD automáticas.
