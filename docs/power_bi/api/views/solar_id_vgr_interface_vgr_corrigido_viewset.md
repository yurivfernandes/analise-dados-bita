# `solar_id_vgr_interface_vgr_corrigido_viewset.py`

## O que é?

Arquivo que define o viewset responsável por expor a API para o modelo `SolarIDVGRInterfaceCorrigido` do app **power_bi**.

---

## Código explicado ponto a ponto

```python
from rest_framework.viewsets import ModelViewSet
from app.utils.paginators import CustomLargePagination
from ...models import SolarIDVGRInterfaceCorrigido
from ..serializers import SolarIDVGRInterfaceCorrigidoSerializer
```
- Importa o `ModelViewSet` do DRF para operações CRUD.
- Importa o paginador customizado.
- Importa o modelo e seu serializer específico.

```python
class SolarIDVGRInterfaceVGRCorrigido(ModelViewSet):
    serializer_class = SolarIDVGRInterfaceCorrigidoSerializer
    queryset = SolarIDVGRInterfaceCorrigido.objects.using("power_bi").all()
    pagination_class = CustomLargePagination
```
- Define a classe viewset usando o serializer específico para `SolarIDVGRInterfaceCorrigido`.
- Configura o queryset para usar o banco "power_bi".
- Utiliza paginação customizada para grandes volumes de dados.

---

## Funcionamento esperado

- A view expõe endpoints RESTful para listar, criar, atualizar e deletar registros.
- Usa o serializer específico para o modelo `SolarIDVGRInterfaceCorrigido`.
- As respostas são paginadas conforme definido em `CustomLargePagination`.

---

## O que pode e não pode alterar

- **Pode**: Customizar o queryset, trocar o serializer, alterar o paginador, sobrescrever métodos para lógica customizada.
- **Não pode**: Remover a herança de `ModelViewSet` se quiser manter as operações CRUD automáticas.
