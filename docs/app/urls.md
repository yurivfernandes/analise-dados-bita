# `urls.py`

## O que é?

Arquivo de roteamento principal do Django. Ele define como as URLs recebidas pelo servidor são encaminhadas para as views corretas do projeto.

---

## Para que serve?

- Centraliza o roteamento das requisições HTTP.
- Permite incluir rotas de diferentes apps de forma modular.
- Facilita a manutenção e expansão do projeto.

---

## Código explicado

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/access/", include("access.api.urls")),
    path("api/power-bi/", include("power_bi.api.urls")),
    path("api/dw-analytics/", include("dw_analytics.api.urls")),
]
```

### Linha a linha

- `from django.contrib import admin`: Importa o módulo de administração do Django.
- `from django.urls import include, path`: Importa funções para definir rotas (`path`) e incluir outros arquivos de rotas (`include`).

- `urlpatterns = [...]`: Lista de todas as rotas do projeto.

    - `path("admin/", admin.site.urls)`: Rota padrão do Django Admin, acessível em `/admin/`.
    - `path("api/access/", include("access.api.urls"))`: Inclui todas as rotas definidas em `access/api/urls.py` sob o prefixo `/api/access/`.
    - `path("api/power-bi/", include("power_bi.api.urls"))`: Inclui as rotas do app `power_bi` sob `/api/power-bi/`.
    - `path("api/dw-analytics/", include("dw_analytics.api.urls"))`: Inclui as rotas do app `dw_analytics` sob `/api/dw-analytics/`.

---

## Como adicionar novas URLs

### 1. Criar um novo app (se necessário)

```bash
python manage.py startapp meu_app
```

### 2. Criar um arquivo de rotas no app

No diretório do app, crie um arquivo `api/urls.py` (ou `urls.py`):

```python
from django.urls import path
from .views import MinhaView

urlpatterns = [
    path("minha-rota/", MinhaView.as_view(), name="minha-rota"),
]
```

### 3. Incluir as rotas do novo app no `urls.py` principal

Adicione uma linha em `urlpatterns`:

```python
path("api/meu-app/", include("meu_app.api.urls")),
```

Agora, todas as rotas definidas em `meu_app/api/urls.py` estarão disponíveis sob `/api/meu-app/`.

---

## O que pode e não pode alterar

- **Pode**:
  - Adicionar novas rotas com `path(...)`.
  - Incluir rotas de novos apps usando `include(...)`.
- **Não pode**:
  - Remover o admin ou rotas essenciais sem saber as consequências.
  - Alterar o nome dos arquivos de rotas sem atualizar os imports.

---

## Por quê?

- Remover rotas essenciais pode impedir o acesso ao admin ou APIs.
- Adicionar rotas corretamente mantém o projeto organizado e modular.
