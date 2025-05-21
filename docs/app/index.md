# Documentação do Módulo `app`

Este módulo contém a configuração principal do projeto Django, incluindo roteamento, configuração de bancos de dados, middlewares, settings globais e utilitários.

## Arquivos Principais

- [`asgi.py`](./asgi.md): Interface assíncrona do Django.
- [`wsgi.py`](./wsgi.md): Interface síncrona (WSGI) do Django.
- [`settings.py`](./settings.md): Configurações globais do projeto.
- [`urls.py`](./urls.md): Roteamento principal do projeto.
- [`database_router.py`](./database_router.md): Roteamento de múltiplos bancos de dados.

## Estrutura de Utilitários

Veja também a documentação em [`utils/`](./utils/) para detalhes sobre utilitários como pipelines e paginação.
- Define a variável `application` para uso por servidores WSGI.
- Carrega as configurações do Django a partir de `app.settings`.

### `settings.py`
Arquivo central de configuração do Django. Define todas as configurações globais do projeto, incluindo:

- Caminhos de diretórios (`BASE_DIR`)
- Configurações de banco de dados (multi-database)
- Apps instalados
- Middlewares
- Configurações de autenticação, CORS, REST Framework, arquivos estáticos e media
- Configurações de internacionalização e timezone

### `urls.py`
Arquivo de roteamento principal do projeto. Define as rotas globais, incluindo:

- Rota para o admin (`/admin/`)
- Inclusão das rotas dos apps: `access`, `power_bi`, `dw_analytics`

### `database_router.py`
Define a classe `MultiDBRouter`, responsável por direcionar operações de leitura, escrita e migração para os bancos corretos conforme o app/model.

- Permite múltiplos bancos de dados no projeto.
- Direciona operações de `dw_analytics` e `power_bi` para seus respectivos bancos.
- Permite relações apenas entre objetos do mesmo banco.

## Estrutura de Utilitários

Veja também a documentação em [`utils/`](./utils/) para detalhes sobre utilitários como pipelines e paginação.
