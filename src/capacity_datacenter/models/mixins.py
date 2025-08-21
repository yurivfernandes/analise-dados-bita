from django.db import models
from ..middleware import get_current_user


class AuditMixin(models.Model):
    """Mixin abstrato que adiciona created_at, updated_at e user.

    O campo `user` é salvo automaticamente no `save()` usando o usuário retornado por
    `capacity_datacenter.middleware.get_current_user()` quando disponível.
    """

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    # armazenamos como VARCHAR(255) por compatibilidade; pode ser alterado para FK
    user = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        try:
            current_user = get_current_user()
            if current_user is not None:
                # tenta obter username ou id como fallback
                username = getattr(current_user, "username", None) or str(getattr(current_user, "id", ""))
                if username:
                    self.user = username
        except Exception:
            # Não romper o fluxo de salvar caso middleware não esteja presente
            pass
        return super().save(*args, **kwargs)
