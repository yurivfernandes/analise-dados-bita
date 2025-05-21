# `database_router.py`

## O que é?

Arquivo que define a lógica de roteamento para múltiplos bancos de dados no Django.

## Para que serve?

Permite que diferentes apps usem diferentes bancos de dados para leitura, escrita e migração.

## Trecho de código explicado

```python
class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "dw_analytics":
            return "dw_analytics"
        elif model._meta.app_label == "power_bi":
            return "power_bi"
        return None
    # ... outros métodos ...
```
- Direciona operações de leitura/escrita/migração para o banco correto com base no app.

## O que pode e não pode alterar

- **Pode**: Adicionar novas regras para novos apps/bancos.
- **Não pode**: Remover métodos obrigatórios (`db_for_read`, `db_for_write`, `allow_migrate`).

## Por quê?

Sem esses métodos, o Django não consegue decidir para qual banco enviar as operações, podendo causar erros graves.
