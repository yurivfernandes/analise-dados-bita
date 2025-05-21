# `mixin.py`

## O que é?

Arquivo que define a classe `MixinViews`, um mixin utilitário para views e pipelines do app **power_bi**. Ele centraliza métodos comuns para manipulação de datas, validação, transformação de dados e integração entre Django ORM e DataFrames Polars.

---

## Estrutura geral do arquivo

### Imports

- `from datetime import datetime`: Para manipulação e validação de datas.
- `import polars as pl`: Para uso de DataFrames Polars, que são eficientes para processamento de dados em memória.
- `from django.db import models`: Para trabalhar com models do Django.
- `from rest_framework.request import Request`, `from rest_framework.response import Response`: Para tipos do Django REST Framework em views.

---

## Classe principal: `MixinViews`

A classe `MixinViews` é um mixin, ou seja, uma classe utilitária para ser herdada por outras classes (views, pipelines, tasks) que precisam de métodos comuns para manipulação de dados.

---

## Métodos detalhados

### 1. `get(self, request: Request, *args, **kwargs) -> Response`
- **O que faz:** Método abstrato para ser implementado em subclasses de views. Deve retornar um objeto `Response` do DRF.
- **Como usar:** Implemente este método em sua view herdada para definir o comportamento do endpoint GET.

### 2. `main(self) -> list`
- **O que faz:** Método abstrato para ser implementado em pipelines ou tasks. Deve retornar uma lista de resultados.
- **Como usar:** Implemente este método em sua pipeline herdada para definir o processamento principal.

### 3. `valid_date(self, data_inicio: str, data_fim: str)`
- **O que faz:** Valida se as datas de início e fim são válidas e no formato correto (`aaaa-mm-dd`). Lança exceções amigáveis se as datas forem inválidas ou inconsistentes.
- **Como usar:** Chame este método antes de processar filtros por data em pipelines ou views.
- **Exemplo:**
  ```python
  data_inicio, data_fim = self.valid_date("2024-01-01", "2024-01-31")
  ```

### 4. `get_dataset(self, query_set: models.QuerySet, schema: dict) -> pl.DataFrame`
- **O que faz:** Converte um queryset Django em um DataFrame Polars, aplicando um schema customizado e renomeando colunas conforme o schema.
- **Como usar:** Use para transformar dados do banco em DataFrame para processamento eficiente.
- **Exemplo:**
  ```python
  df = self.get_dataset(MeuModel.objects.all(), schema)
  ```

### 5. `generate_schema_from_model(self, model: models)`
- **O que faz:** Gera um dicionário de schema a partir dos campos de um model Django, mapeando para tipos Polars.
- **Como usar:** Use para automatizar a criação de schemas para DataFrames.
- **Exemplo:**
  ```python
  schema = self.generate_schema_from_model(MeuModel)
  ```

### 6. `get_polars_type(self, field: models.fields)`
- **O que faz:** Mapeia tipos de campo Django para tipos de dados Polars (ex: `CharField` vira `pl.String`, `IntegerField` vira `pl.Int64`).
- **Como usar:** Usado internamente por `generate_schema_from_model`, mas pode ser sobrescrito para suportar novos tipos.

---

## Como herdar e utilizar o mixin

Para usar os métodos do `MixinViews`, basta herdar a classe na sua view, pipeline ou task:

```python
from power_bi.utils.mixin import MixinViews

class MinhaPipeline(MixinViews):
    def main(self):
        data_inicio, data_fim = self.valid_date("2024-01-01", "2024-01-31")
        schema = self.generate_schema_from_model(model=MeuModel)
        df = self.get_dataset(query_set=MeuModel.objects.all(), schema=schema)
        # ...processamento...
```

- Implemente os métodos abstratos (`get`, `main`) conforme a necessidade da sua classe.
- Os métodos utilitários (`valid_date`, `get_dataset`, etc.) ficam disponíveis para uso direto.

---

## Funcionamento esperado

- O mixin padroniza e centraliza lógica comum, evitando repetição de código em múltiplas views/pipelines.
- Facilita a integração entre Django ORM e Polars, além de garantir validação consistente de datas e schemas.

---

## O que pode e não pode alterar

- **Pode**: Adicionar novos métodos utilitários, sobrescrever métodos abstratos nas subclasses.
- **Não pode**: Remover métodos essenciais se outras classes dependem deles, ou alterar assinaturas sem atualizar todas as subclasses.

---

Consulte o código fonte para detalhes de implementação de cada método.