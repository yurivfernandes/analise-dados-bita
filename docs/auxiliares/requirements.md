# Dependências do Projeto (requirements.txt)

## Django e Django REST Framework

### Core
- **Django==4.2.10** 
  - Framework web principal
  - [Documentação](https://docs.djangoproject.com/en/4.2/)

### APIs e Extensões
- **djangorestframework==3.14.0**
  - Framework para APIs REST
  - [Documentação](https://www.django-rest-framework.org/)
- **django-cors-headers==4.3.1**
  - Gerenciamento de CORS para APIs
- **django-filter==23.5**
  - Filtros avançados para APIs
- **drf-yasg==1.21.7**
  - Documentação automática Swagger/OpenAPI

### Autenticação
- **django-rest-knox==4.2.0**
  - Tokens de autenticação seguros
- **djangorestframework-simplejwt==5.3.1**
  - Autenticação JWT
- **PyJWT**
  - Manipulação de tokens JWT

## Banco de Dados

### SQL Server
- **mssql-django==1.4**
  - Driver Django para SQL Server
- **pyodbc**
  - Conexão ODBC com SQL Server

## Processamento de Dados

### Data Science
- **polars==1.29.0**
  - Framework de processamento de dados de alta performance
  - [Documentação](https://pola-rs.github.io/polars-book/)
- **pandas==1.5.3**
  - Análise e manipulação de dados
  - [Documentação](https://pandas.pydata.org/docs/)

## Utilitários

### HTTP e Redes
- **requests==2.31.0**
  - Cliente HTTP para Python
- **urllib3==2.2.0**, **certifi==2024.2.2**, **charset-normalizer==3.3.2**, **idna==3.6**
  - Dependências para requests e networking

### Configuração
- **python-dotenv==1.0.1**
  - Carregamento de variáveis de ambiente

## Documentação

### MkDocs
- **mkdocs==1.5.3**
  - Geração de documentação estática
  - [Documentação](https://www.mkdocs.org/)
- **mkdocs-material==9.5.12**
  - Tema Material Design para MkDocs
  - [Documentação](https://squidfunk.github.io/mkdocs-material/)
- **mkdocstrings==0.24.0**, **mkdocstrings-python==1.7.5**
  - Geração automática de documentação a partir de docstrings

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## Atualizando Dependências

Para atualizar uma dependência específica:
```bash
pip install --upgrade nome-pacote
pip freeze > requirements.txt
```

## Boas Práticas

1. **Versões Fixas**
   - Use versões específicas (==) para reprodutibilidade
   - Evite ranges de versão (~= ou >=) em produção

2. **Organização**
   - Mantenha dependências agrupadas por função
   - Documente o propósito de cada dependência

3. **Segurança**
   - Atualize regularmente para versões de segurança
   - Use ferramentas como `safety` para verificar vulnerabilidades
```
