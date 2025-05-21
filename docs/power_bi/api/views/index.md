# Views

## O que são views no app power_bi?

Views são responsáveis por receber requisições HTTP, processar dados (consultar banco, aplicar regras de negócio, transformar dados para o Power BI, etc.) e retornar respostas HTTP (geralmente JSON).

- No contexto do **power_bi**, as views normalmente herdam de `ModelViewSet` do Django REST Framework para expor operações CRUD ou de classes customizadas para tarefas específicas.

---

## Estrutura básica de uma view

```python
from rest_framework.viewsets import ModelViewSet
from ...models import TblSolarInterfacesVgr
from ..serializers import SolarInterfacesVgrSerializer

class SolarInterfacesVGR(ModelViewSet):
    serializer_class = SolarInterfacesVgrSerializer
    queryset = TblSolarInterfacesVgr.objects.using("power_bi").all()
```

---

## Como usar e importar views

- Importe as views no `__init__.py` da pasta `views` para facilitar o uso em outros arquivos, como o de rotas (`urls.py`).
- Exemplo:
  ```python
  from .solar_interfaces_vgr import SolarInterfacesVGR
  ```

---

## Funcionamento esperado

- Cada viewset expõe endpoints RESTful para listar, criar, atualizar e deletar registros dos modelos do Power BI.
- As views podem ser customizadas para processar dados antes de retornar para o frontend ou Power BI.

---

Consulte os arquivos individuais para detalhes de cada view.
