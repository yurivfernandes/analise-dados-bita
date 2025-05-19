# Análise de Dados Bita

Este projeto utiliza Django para realizar análises de dados com integração ao banco de dados SQL Server.

## Tecnologias Utilizadas

- Python
- Django
- SQL Server
- ODBC Driver 17 for SQL Server

## Configuração do Ambiente

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd analise-dados-bita
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo `.env` com as credenciais do banco de dados.

5. Execute o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Estrutura do Projeto

- `src/app/`: Contém a configuração principal do projeto Django.
- `.env`: Arquivo para armazenar variáveis de ambiente, como credenciais do banco de dados.

## Contato

Para dúvidas ou sugestões, entre em contato com o desenvolvedor.
