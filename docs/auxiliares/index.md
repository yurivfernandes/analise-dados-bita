# Auxiliares Python & Django

Esta seção reúne explicações e conceitos fundamentais para trabalhar com Django, sua ORM, integração com bancos de dados, geração de APIs REST, pipelines de dados e as principais bibliotecas utilizadas no projeto.

---

## Como funciona o Django

Django é um framework web em Python que segue o padrão MTV (Model-Template-View). Ele facilita o desenvolvimento rápido de aplicações web robustas, seguras e escaláveis.

### Principais características:
- Estrutura modular e reutilizável.
- Admin automático.
- Sistema de autenticação pronto.
- Suporte a múltiplos bancos de dados.
- Integração fácil com APIs REST via Django REST Framework.

---

## Django como ORM

ORM (Object-Relational Mapping) é uma camada que permite manipular dados do banco usando objetos Python, sem escrever SQL manualmente.

- **Modelos Django** representam tabelas do banco.
- **QuerySets** permitem consultar, filtrar, atualizar e deletar dados de forma orientada a objetos.
- **Migrations** sincronizam as alterações dos modelos com o banco de dados.

**Exemplo:**
```python
# models.py
class Cliente(models.Model):
    nome = models.CharField(max_length=100)

# Consulta
clientes = Cliente.objects.filter(nome__icontains="joão")
```

---

## Integração com banco de dados

- O Django suporta diversos bancos (PostgreSQL, MySQL, SQLite, SQL Server).
- A configuração é feita no arquivo `settings.py` em `DATABASES`.
- O projeto utiliza múltiplos bancos, roteados por app via `DATABASE_ROUTERS`.

---

## Geração de APIs REST

- Utilizamos o **Django REST Framework (DRF)** para criar APIs RESTful.
- **Serializers** convertem modelos em JSON e vice-versa.
- **ViewSets** e **Routers** facilitam a criação de endpoints CRUD.
- Permite autenticação, paginação, filtros e permissões customizadas.

**Exemplo:**
```python
from rest_framework import serializers, viewsets

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
```

---

## Pipelines de dados

- Pipelines são classes utilitárias para processar grandes volumes de dados, ETL (Extract, Transform, Load) e integrações.
- Utilizam a classe base `Pipeline` para padronizar logs e execução.
- Podem ser usadas em tasks, comandos customizados ou integradas com Celery.

---

## Bibliotecas utilizadas e para que servem

- **Django**: Framework web principal.
- **djangorestframework**: Criação de APIs REST.
- **django-cors-headers**: Permite requisições de diferentes domínios (CORS).
- **django-filter**: Filtros avançados em APIs.
- **mssql-django**: Suporte ao banco SQL Server.
- **pyodbc**: Driver ODBC para conexão com SQL Server.
- **polars**: Processamento de dados em DataFrames de alta performance.
- **pandas**: Manipulação de dados tabulares (usado em alguns pipelines).
- **python-dotenv**: Carregamento de variáveis de ambiente.
- **drf-yasg**: Geração automática de documentação Swagger/OpenAPI.
- **mkdocs, mkdocs-material, mkdocstrings**: Geração de documentação estática do projeto.

---

## Resumo

- Django permite criar aplicações web e APIs REST de forma rápida e segura.
- A ORM facilita o trabalho com bancos de dados sem SQL manual.
- O projeto integra processamento de dados eficiente (Polars/Pandas) e múltiplos bancos.
- Bibliotecas auxiliares garantem segurança, performance e documentação de qualidade.

Consulte os subdiretórios para detalhes sobre tipos de dados, exemplos de uso e melhores práticas.
