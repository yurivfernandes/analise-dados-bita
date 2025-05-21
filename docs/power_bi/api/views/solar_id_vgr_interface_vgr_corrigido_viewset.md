# `solar_id_vgr_interface_vgr_corrigido_viewset.py`

## O que é?

Arquivo que define o viewset responsável por expor a API para o modelo `SolarIDVGRInterfaceCorrigido` do app **power_bi**.

---

## Código explicado ponto a ponto

```python
from rest_framework.viewsets import ModelViewSet
```
- Importa o `ModelViewSet` do Django REST Framework, que já implementa todas as operações CRUD.

```python
from app.utils.paginators import CustomLargePagination
```
- Importa um paginador customizado.

```python
from ...models import SolarIDVGRInterfaceCorrigido
from ..serializers import SolarInterfacesVgrSerializer
```
- Importa o modelo `SolarIDVGRInterfaceCorrigido`.
- Importa o serializer, responsável por converter o modelo em JSON para a API.

```python
class SolarIDVGRInterfaceVGRCorrigido(ModelViewSet):
    serializer_class = SolarInterfacesVgrSerializer
    queryset = SolarIDVGRInterfaceCorrigido.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
```
- Define a classe `SolarIDVGRInterfaceVGRCorrigido`, herdando de `ModelViewSet`.
- `serializer_class`: Indica qual serializer será usado.
- `queryset`: Define o conjunto de dados exposto pela API, usando o banco correto.
- `pagination_class`: Define o paginador.

---

## Funcionamento esperado

- A view expõe endpoints RESTful para listar, criar, atualizar e deletar registros de `SolarIDVGRInterfaceCorrigido`.
- As respostas são paginadas conforme definido em `CustomLargePagination`.

---

## O que pode e não pode alterar

- **Pode**: Customizar o queryset, trocar o serializer, alterar o paginador, sobrescrever métodos para lógica customizada.
- **Não pode**: Remover a herança de `ModelViewSet` se quiser manter as operações CRUD automáticas.
