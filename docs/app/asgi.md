# `asgi.py`

## O que é?

Arquivo de configuração para ASGI (Asynchronous Server Gateway Interface), padrão moderno para aplicações Python assíncronas.

## Para que serve?

Permite que o Django rode em servidores assíncronos, suportando WebSockets, HTTP2 e outras features modernas.

## Trecho de código explicado

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_asgi_application()
```
- Define a variável de ambiente para as configurações do Django.
- Cria a aplicação ASGI a partir das configurações.

## O que pode e não pode alterar

- **Pode**: Alterar o nome do módulo de settings se o projeto mudar de estrutura.
- **Não pode**: Remover a definição de `application`, pois é o ponto de entrada do servidor ASGI.

## Por quê?

A ausência ou alteração incorreta deste arquivo impede o deploy em servidores assíncronos.
