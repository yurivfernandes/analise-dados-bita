# Análise de Dados Bita

Este projeto utiliza Django para realizar análises de dados com integração ao banco de dados SQL Server.

## Tecnologias Utilizadas

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red?logo=django)](https://www.django-rest-framework.org/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-ODBC_17-blue?logo=microsoftsqlserver)](https://learn.microsoft.com/sql/)
[![PyODBC](https://img.shields.io/badge/pyodbc-4.0-orange?logo=databricks)](https://github.com/mkleehammer/pyodbc)
[![Polars](https://img.shields.io/badge/Polars-1.29-purple?logo=python)](https://www.pola.rs/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5.3-white?logo=pandas)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-latest-informational?logo=numpy)](https://numpy.org/)
[![Celery](https://img.shields.io/badge/Celery-5.2.7-darkgreen?logo=celery)](https://docs.celeryq.dev/)
[![MkDocs](https://img.shields.io/badge/MkDocs-Material-9.5.12-yellow?logo=markdown)](https://squidfunk.github.io/mkdocs-material/)
[![JWT](https://img.shields.io/badge/JWT-PyJWT-green?logo=jsonwebtokens)](https://pyjwt.readthedocs.io/)
[![Meraki](https://img.shields.io/badge/Meraki-API-2.0.3-blue?logo=cisco)](https://developer.cisco.com/meraki/)

## Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd analise-dados-bita
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com as credenciais do banco de dados.

5. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Estrutura do Projeto

- `src/app/`: Contém a configuração principal do projeto Django.
- `.env`: Arquivo para armazenar variáveis de ambiente, como credenciais do banco de dados.

## Contato

Para dúvidas ou sugestões, entre em contato com o desenvolvedor.
