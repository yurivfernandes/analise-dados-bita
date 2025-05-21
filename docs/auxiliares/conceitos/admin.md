# Django Admin

## O que é o Admin?

O Django Admin é uma interface administrativa automática que permite gerenciar os dados do seu modelo através de uma interface web.

## Configuração Básica

```python
from django.contrib import admin

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'estoque']
    list_filter = ['categoria']
    search_fields = ['nome']
    ordering = ['-criado_em']
```

## Customização

```python
class PedidoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vendedor=request.user)
```
