# `settings.py`

## O que é?

Arquivo central de configuração do Django. Ele define todas as variáveis e parâmetros que controlam o funcionamento do projeto, desde bancos de dados até autenticação, localização, arquivos estáticos e apps instalados.

---

## Para que serve?

- Centralizar todas as configurações do projeto.
- Permitir fácil customização do ambiente (desenvolvimento, produção, testes).
- Garantir que todos os apps e integrações funcionem corretamente.

---

## Explicação ponto a ponto

### 1. Imports e carregamento de variáveis de ambiente

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
```
- `os` e `Path` são usados para manipular caminhos e variáveis do sistema.
- `load_dotenv()` carrega variáveis do arquivo `.env` para proteger dados sensíveis (senhas, usuários, etc).

---

### 2. Diretório base do projeto

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```
- Define o diretório raiz do projeto, usado para construir caminhos relativos (ex: arquivos estáticos, media).

---

### 3. Segurança

```python
SECRET_KEY = "django-insecure-..."
DEBUG = True
ALLOWED_HOSTS = []
```
- `SECRET_KEY`: Chave secreta usada para criptografia interna do Django.
- `DEBUG`: Ativa/desativa modo debug (NUNCA deixe True em produção).
- `ALLOWED_HOSTS`: Lista de domínios permitidos para acessar o projeto.

---

### 4. Apps instalados

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",  # CORS para requisições externas
    "rest_framework",  # Django REST Framework
    "django_filters",  # Filtros para APIs
    "rest_framework.authtoken",  # Autenticação por token
    "access",  # App de autenticação customizado
    "dw_analytics",  # App de analytics
    "power_bi",  # App de integração Power BI
]
```
- Cada string é o nome de um app Django.
- **Para adicionar um novo app**: crie o app com `python manage.py startapp nome_do_app` e adicione `"nome_do_app"` à lista.
- **Por quê?**: Só apps listados aqui são reconhecidos pelo Django (migrações, admin, etc).

---

### 5. Middlewares

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```
- Middlewares são camadas intermediárias que processam requisições e respostas.
- **Ordem importa**: CORS deve vir antes de outros middlewares para funcionar corretamente.

---

### 6. URLs e Templates

```python
ROOT_URLCONF = "app.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "app.wsgi.application"
```
- `ROOT_URLCONF`: Arquivo principal de rotas.
- `TEMPLATES`: Configuração do sistema de templates do Django.
- `WSGI_APPLICATION`: Ponto de entrada para servidores WSGI.

---

### 7. Bancos de dados

```python
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("DB_NAME_APLICATION"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "1433"),
        "OPTIONS": {
            "driver": os.getenv("DB_DRIVER", "SQL Server Native Client 11.0"),
            "Trusted_Connection": "yes",
        },
    },
    "dw_analytics": {...},
    "power_bi": {...},
}
DATABASE_ROUTERS = ["app.database_router.MultiDBRouter"]
```
- Permite múltiplos bancos de dados, cada um com suas credenciais.
- `DATABASE_ROUTERS` define a lógica para direcionar queries para o banco correto.
- **Não remova**: Essencial para o funcionamento dos apps que usam bancos separados.

---

### 8. Validação de senha

```python
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
```
- Define regras para senhas de usuários.

---

### 9. Internacionalização

```python
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
```
- Configura idioma e fuso horário padrão.

---

### 10. Arquivos estáticos e media

```python
STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "cadastro/arquivos"
```
- Define onde arquivos estáticos e uploads de usuários são armazenados.

---

### 11. Chave primária padrão

```python
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```
- Define o tipo padrão de campo para chaves primárias.

---

### 12. Usuário customizado

```python
AUTH_USER_MODEL = "access.User"
```
- Define o modelo de usuário customizado do app `access`.

---

### 13. CORS

```python
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```
- Permite requisições de origens externas (ex: frontend em React).

---

### 14. Django REST Framework

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```
- Configura paginação, autenticação, filtros e permissões padrão para APIs.

---

### 15. Filtros

```python
FILTERS_DEFAULT_LOOKUP_EXPR = "icontains"
```
- Define o lookup padrão para filtros (busca insensível a maiúsculas/minúsculas).

---

## O que pode e não pode alterar

- **Pode**:
  - Adicionar apps em `INSTALLED_APPS`.
  - Adicionar middlewares.
  - Alterar variáveis de ambiente para bancos de dados.
  - Customizar configurações do REST Framework conforme necessidade.

- **Não pode**:
  - Remover variáveis essenciais (`DATABASES`, `INSTALLED_APPS`, `ROOT_URLCONF`, `WSGI_APPLICATION`).
  - Alterar `SECRET_KEY` em produção sem migrar tokens/senhas.
  - Deixar `DEBUG=True` em produção.

---

## Como adicionar um novo app

1. Crie o app:
   ```bash
   python manage.py startapp nome_do_app
   ```
2. Adicione `"nome_do_app"` em `INSTALLED_APPS`.
3. (Opcional) Crie rotas e inclua no arquivo de URLs principal.

**Por quê?**  
Sem adicionar o app, o Django não reconhece modelos, rotas ou comandos do novo app.

---
