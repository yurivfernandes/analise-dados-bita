# Modelos DW Analytics

## O que são models no Django?

Models são classes Python que representam tabelas do banco de dados. Cada atributo da classe corresponde a uma coluna da tabela, e cada instância da classe representa uma linha (registro) da tabela.

---

## Paralelo com SQL

- **Model Django** = **Tabela SQL**
- **Campo do model** = **Coluna da tabela**
- **Instância do model** = **Linha/registro da tabela**

Exemplo:
```python
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
```
Equivalente em SQL:
```sql
CREATE TABLE cliente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    idade INTEGER
);
```

---

## Tipos de dados em models Django

Veja a página [Tipos de Dados em Models Django](./tipos_de_dados.md) para uma explicação detalhada dos tipos de campos disponíveis, exemplos de uso e paralelos com SQL.

---

## Para que servem?

- Definir a estrutura dos dados do seu sistema.
- Permitir que o Django crie, altere e remova tabelas automaticamente via migrations.
- Facilitar consultas, inserções, atualizações e deleções usando Python, sem escrever SQL manualmente.

---

## Como o Django trabalha com models

- O Django converte cada model em uma tabela no banco de dados.
- Usa as models para gerar formulários, serializers, admin, etc.
- Permite consultar e manipular dados usando a ORM (Object-Relational Mapping).

Exemplo de consulta:
```python
clientes = Cliente.objects.filter(idade__gte=18)
```
Equivalente em SQL:
```sql
SELECT * FROM cliente WHERE idade >= 18;
```

---

## Como usar models em views ou pipelines (tasks)

- Em views, você pode consultar, criar ou atualizar registros usando a model:
    ```python
    from .models import Cliente

    def listar_clientes_maiores(request):
        maiores = Cliente.objects.filter(idade__gte=18)
        # ...retornar resposta...
    ```
- Em pipelines/tasks, use as models para ler ou gravar dados durante o processamento:
    ```python
    from .models import Cliente

    def processar_clientes():
        for cliente in Cliente.objects.all():
            # ...processamento...
    ```

---

## Como criar um model

1. Crie uma classe que herda de `models.Model`:
    ```python
    from django.db import models

    class Produto(models.Model):
        nome = models.CharField(max_length=100)
        preco = models.DecimalField(max_digits=10, decimal_places=2)
    ```
2. Adicione o model ao arquivo `models/__init__.py` para facilitar os imports:
    ```python
    from .produto import Produto
    ```
3. Rode `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco.

---

## Boas práticas e pontos importantes

- Sempre defina o campo `Meta: db_table` se quiser controlar o nome da tabela no banco.
- Use `app_label` em projetos multi-app para garantir que o Django reconheça o app correto.
- Prefira nomes de campos e tabelas em inglês para projetos internacionais, mas siga o padrão do projeto.
- Utilize métodos customizados no model para regras de negócio relacionadas àquela tabela.
- Models podem ter relacionamentos (`ForeignKey`, `ManyToManyField`, etc.), representando chaves estrangeiras e tabelas de associação no SQL.

---

## Resumo

- Models são a base do mapeamento entre Python e SQL no Django.
- Permitem manipular dados do banco de forma orientada a objetos.
- São essenciais para views, serializers, pipelines e qualquer lógica de dados do projeto.

Consulte os arquivos individuais para detalhes de cada modelo.
- Permite consultar e manipular dados usando a ORM (Object-Relational Mapping).

Exemplo de consulta:
```python
clientes = Cliente.objects.filter(idade__gte=18)
```
Equivalente em SQL:
```sql
SELECT * FROM cliente WHERE idade >= 18;
```

---

## Como usar models em views ou pipelines (tasks)

- Em views, você pode consultar, criar ou atualizar registros usando a model:
    ```python
    from .models import Cliente

    def listar_clientes_maiores(request):
        maiores = Cliente.objects.filter(idade__gte=18)
        # ...retornar resposta...
    ```
- Em pipelines/tasks, use as models para ler ou gravar dados durante o processamento:
    ```python
    from .models import Cliente

    def processar_clientes():
        for cliente in Cliente.objects.all():
            # ...processamento...
    ```

---

## Como criar um model

1. Crie uma classe que herda de `models.Model`:
    ```python
    from django.db import models

    class Produto(models.Model):
        nome = models.CharField(max_length=100)
        preco = models.DecimalField(max_digits=10, decimal_places=2)
    ```
2. Adicione o model ao arquivo `models/__init__.py` para facilitar os imports:
    ```python
    from .produto import Produto
    ```
3. Rode `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco.

---

## Boas práticas e pontos importantes

- Sempre defina o campo `Meta: db_table` se quiser controlar o nome da tabela no banco.
- Use `app_label` em projetos multi-app para garantir que o Django reconheça o app correto.
- Prefira nomes de campos e tabelas em inglês para projetos internacionais, mas siga o padrão do projeto.
- Utilize métodos customizados no model para regras de negócio relacionadas àquela tabela.
- Models podem ter relacionamentos (`ForeignKey`, `ManyToManyField`, etc.), representando chaves estrangeiras e tabelas de associação no SQL.

---

## Resumo

- Models são a base do mapeamento entre Python e SQL no Django.
- Permitem manipular dados do banco de forma orientada a objetos.
- São essenciais para views, serializers, pipelines e qualquer lógica de dados do projeto.

Consulte os arquivos individuais para detalhes de cada modelo.
