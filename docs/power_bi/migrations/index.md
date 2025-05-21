# Migrations

## O que são migrations?

Migrations são arquivos gerados pelo Django que registram e controlam todas as alterações feitas na estrutura do banco de dados (schema) do app **power_bi**. Elas funcionam como um "histórico versionado" das tabelas, campos e relacionamentos do seu projeto.

---

## Para que servem?

- **Criar** tabelas e campos no banco de dados automaticamente.
- **Alterar** a estrutura existente (adicionar/remover campos, mudar tipos, criar índices, etc).
- **Remover** tabelas/campos que não são mais necessários.
- **Sincronizar** o código Python dos modelos com o banco de dados real.

---

## Quando fazer uma migration?

- Sempre que você criar, alterar ou remover um modelo ou campo em qualquer arquivo `models.py` do app.
- Exemplo: adicionou um campo novo em um modelo? Rode `python manage.py makemigrations power_bi`.

---

## Como funcionam?

- O Django compara o estado atual dos modelos Python com o histórico de migrations já aplicadas.
- Gera um novo arquivo de migration descrevendo as mudanças.
- Ao rodar `python manage.py migrate`, o Django executa as operações no banco de dados conforme descrito nas migrations.

---

## Como entender o código de uma migration?

- Cada migration é uma classe com uma lista de operações (`operations = [...]`).
- Exemplos de operações:
  - `CreateModel`: Cria uma nova tabela/modelo.
  - `AddField`: Adiciona um campo a uma tabela existente.
  - `AlterField`: Altera o tipo ou opções de um campo.
  - `RemoveField`: Remove um campo de uma tabela.
  - `DeleteModel`: Remove uma tabela/modelo.
  - `RenameField`: Renomeia um campo existente.

Exemplo:
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='MinhaTabela',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='outratabela',
            name='novo_campo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='outratabela',
            name='campo_existente',
            field=models.CharField(max_length=200),
        ),
        migrations.RemoveField(
            model_name='outratabela',
            name='campo_antigo',
        ),
        migrations.DeleteModel(
            name='TabelaAntiga',
        ),
        migrations.RenameField(
            model_name='minhatabela',
            old_name='nome_antigo',
            new_name='nome_novo',
        ),
    ]
```

---

## Boas práticas

- Sempre faça commit dos arquivos de migration junto com as alterações nos modelos.
- Não edite migrations antigas manualmente (exceto em casos muito específicos e com cuidado).
- Use `makemigrations` para gerar e `migrate` para aplicar as mudanças.
- Mantenha o histórico de migrations para facilitar rollback e auditoria.

---

Consulte os arquivos individuais para detalhes de cada migration.
