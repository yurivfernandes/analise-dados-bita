# `wsgi.py`

## O que é?

Arquivo de configuração para WSGI (Web Server Gateway Interface), padrão tradicional para aplicações web Python síncronas.

## Para que serve?

Permite que o Django rode em servidores como Gunicorn, uWSGI, Apache mod_wsgi, etc.

## Trecho de código explicado

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()
```
- Define a variável de ambiente para as configurações do Django.
- Cria a aplicação WSGI a partir das configurações.

## O que pode e não pode alterar

- **Pode**: Alterar o nome do módulo de settings se necessário.
- **Não pode**: Remover a definição de `application`.

## Por quê?

Sem esse arquivo, o deploy em servidores WSGI não funciona.
