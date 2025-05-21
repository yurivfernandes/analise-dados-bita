# Django Migrations

## O que são Migrations?

Migrations são o sistema do Django para propagar mudanças feitas nos models para o esquema do banco de dados.

## Comandos Básicos

```bash
# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Listar migrations
python manage.py showmigrations
```

## Migration Manual

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='preco',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
```
