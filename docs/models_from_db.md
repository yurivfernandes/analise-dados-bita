# Gerar Models a partir de um Banco de Dados Existente

Se o banco de dados já possui tabelas criadas, você pode gerar automaticamente as models no Django utilizando o comando `inspectdb`.

## Passos para Gerar Models

1. Certifique-se de que o banco de dados está configurado corretamente no arquivo `settings.py` e que as credenciais estão no `.env`.

2. Execute o comando abaixo para inspecionar o banco de dados e gerar as models:
   ```bash
   python manage.py inspectdb > app/models.py
   ```

   Isso criará um arquivo `models.py` com as definições das tabelas existentes no banco.

3. Revise o arquivo gerado e ajuste as models conforme necessário. Por exemplo:
   - Adicione `verbose_name` ou `help_text` para melhorar a documentação.
   - Ajuste os relacionamentos entre tabelas, se necessário.

4. Após revisar as models, aplique as migrações para sincronizar o estado do banco com as models:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Observação

- O comando `inspectdb` é útil para iniciar o processo de modelagem, mas pode ser necessário ajustar manualmente as models para atender às necessidades do projeto.
- Certifique-se de que o driver ODBC está instalado e configurado corretamente para acessar o banco de dados.
