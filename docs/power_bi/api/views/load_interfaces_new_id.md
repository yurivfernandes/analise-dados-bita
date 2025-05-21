# `load_interfaces_new_id.py`

## O que é?

Arquivo que define a view responsável por acionar a task de construção da base consolidada de interfaces no app **power_bi**.

---

## Código explicado ponto a ponto

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from ...tasks import LoadInterfaceNewID
```
- Importa a `APIView` do DRF para criar uma view baseada em classe.
- Importa o `Response` para retornar respostas HTTP.
- Importa a task `LoadInterfaceNewID` responsável pelo processamento dos dados.

```python
class LoadInterfaceNewIDVGR(APIView):
    """View que aciona a task de construção da base de [Consolidacao]"""

    def post(self, request, *args, **kwargs) -> Response:
        filtros = {
            "company_remedy_list": request.data.get("company_remedy", []),
            "nome_do_cliente_list": request.data.get("nome_do_cliente", []),
        }

        with LoadInterfaceNewID(**filtros) as load:
            log = load.run()
        return Response(log)
```
- Define a classe `LoadInterfaceNewIDVGR`, herdando de `APIView`.
- O método `post` recebe dados do request, monta filtros e executa a task `LoadInterfaceNewID` usando um context manager.
- Retorna o log do processamento como resposta.

---

## Funcionamento esperado

- Ao receber uma requisição POST, executa a pipeline de carga e transformação de dados.
- Retorna um log detalhado da execução.

---

## O que pode e não pode alterar

- **Pode**: Customizar os filtros, adicionar validações, alterar o retorno.
- **Não pode**: Remover a chamada da task se quiser manter o processamento automatizado.
