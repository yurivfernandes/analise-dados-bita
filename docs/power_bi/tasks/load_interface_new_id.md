# `load_interface_new_id.py`

## O que é?

Arquivo que define a task `LoadInterfaceNewID`, responsável por extrair, transformar e carregar dados de interfaces do Solar para a base consolidada, além de manter logs detalhados do processo.

---

## Estrutura geral do arquivo

### Imports

```python
from functools import cached_property
import polars as pl
from django.db import connection, models, transaction
from django.utils.functional import cached_property
from app.utils.pipeline import Pipeline
from ..models import SolarIDVGRInterfaceCorrigido, TblSolarInterfacesVgr
from ..utils.mixin import MixinViews
```
- Importa funções utilitárias, biblioteca de DataFrame (`polars`), recursos do Django para banco de dados e transações, pipeline base, models e mixins de utilidades.

---

### Classe principal: `LoadInterfaceNewID`

```python
class LoadInterfaceNewID(MixinViews, Pipeline):
    """Extrai, transforma e carrega os dados de Receita Consolidados."""
    # ...existing code...
```
- Herda de `MixinViews` (métodos utilitários para manipulação de dados) e `Pipeline` (padronização de logs e execução).
- Centraliza toda a lógica de ETL (Extract, Transform, Load) para interfaces Solar.

---

### Principais métodos e propriedades

- **`__init__`**: Recebe listas de filtros via kwargs para limitar o escopo dos dados processados.
- **`_get_solar_interface_vgr_queryset`**: Retorna o queryset filtrado do modelo `TblSolarInterfacesVgr`.
- **`_filtro`**: Propriedade que monta o dicionário de filtros a partir dos parâmetros recebidos.
- **`schema`**: Propriedade que gera o schema do DataFrame a partir do modelo.
- **`solar_interface_dataset`**: Propriedade que retorna um DataFrame Polars com os dados filtrados.
- **`run`**: Método principal que executa as etapas de extração, transformação e carga, retornando o log.
- **`extract_transform_dataset`**: Realiza a transformação dos dados, incluindo a busca de IDs finais e histórico.
- **`get_final_id_vgr`**: Busca recursivamente o ID final e mantém um log de IDs históricos.
- **`query_sae`**: Executa uma query SQL para buscar o novo ID e status no banco externo.
- **`load`**: Executa a carga dos dados, usando transações para garantir atomicidade.
- **`_delete`** e **`_save`**: Métodos auxiliares para deletar e inserir registros no banco de destino.

---

### Exemplo de uso

```python
from power_bi.tasks import LoadInterfaceNewID

with LoadInterfaceNewID(company_remedy_list=[...], nome_do_cliente_list=[...]) as task:
    log = task.run()
print(log)
```
- O uso do context manager (`with`) garante que o log será preenchido corretamente, mesmo em caso de erro.

---

## Funcionamento esperado

- Executa todas as etapas de ETL (extração, transformação, carga) e retorna um log detalhado.
- Pode ser chamada por views, comandos ou agendada via Celery.
- Permite fácil customização dos filtros e lógica de transformação.

---

## Explicação detalhada dos principais pontos

- **Filtros dinâmicos**: Os filtros são passados via kwargs e aplicados ao queryset, permitindo processar apenas subconjuntos dos dados.
- **Uso de Polars**: O processamento dos dados é feito em DataFrames Polars, que são mais rápidos e eficientes para grandes volumes de dados.
- **Busca de IDs finais**: O método `get_final_id_vgr` faz chamadas recursivas ao banco externo para encontrar o ID final e monta um histórico de todos os IDs percorridos.
- **Carga transacional**: O método `load` usa `@transaction.atomic` para garantir que a deleção e inserção dos dados sejam atômicas, evitando inconsistências.
- **Log padronizado**: Toda execução gera um log com número de registros inseridos/deletados, tempo de execução e status.

---

## O que pode e não pode alterar

- **Pode**: Customizar filtros, lógica de transformação, adicionar validações, alterar o modelo de destino, modificar queries SQL conforme necessidade.
- **Não pode**: Remover a herança de `Pipeline` se quiser manter logs padronizados e suporte a context manager. Não remova o uso de transações se quiser garantir atomicidade.

---

## Integração com views e APIs

- A task pode ser chamada diretamente por uma view (exemplo: `LoadInterfaceNewIDVGR`), permitindo que o processamento seja disparado por uma requisição HTTP.
- O log retornado pode ser usado para monitoramento e auditoria do processo.

---

Consulte o código fonte para detalhes de implementação de cada método.
