import threading

_local = threading.local()


class CurrentUserMiddleware:
    """Middleware simples que guarda o usuário atual em thread-local.

    Adicione em `MIDDLEWARE` do settings.py: 'capacity_datacenter.middleware.CurrentUserMiddleware'
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # armazena o usuário (pode ser AnonymousUser)
        _local.user = getattr(request, "user", None)
        try:
            response = self.get_response(request)
            return response
        finally:
            _local.user = None


def get_current_user():
    """Retorna o usuário armazenado no contexto atual (ou None)."""
    return getattr(_local, "user", None)
