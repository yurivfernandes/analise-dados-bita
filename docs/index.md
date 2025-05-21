# Análise de Dados BITA

## Visão Geral

Este é um projeto Django que fornece diversas API's e pipelines para análise de dados do BITA. O projeto é organizado em três principais aplicações por ora:

- **Access**: Gerenciamento de autenticação e usuários
- **DW Analytics**: Análise de dados do Data Warehouse
- **Power BI**: Integração com Power BI e análises específicas


## Estrutura Detalhada do Projeto

```text
src/
├── access/                     # App de autenticação e usuários
│   ├── api/                   
│   │   ├── views/            
│   │   │   ├── __init__.py
│   │   │   └── user_views.py 
│   │   └── urls.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py          # Criação do modelo User
│   │   ├── 0002_user_full_name.py   # Adição do campo full_name
│   │   └── 0003_user_company.py     # Adição do campo company_name
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py           # Modelo personalizado de usuário
│   ├── __init__.py
│   ├── admin.py              # Configurações do admin
│   ├── apps.py              
│   └── forms.py              # Formulários personalizados
├── app/                       # Configurações principais
│   ├── settings.py           # Configurações do Django
│   ├── urls.py               # URLs principais
│   ├── wsgi.py               # Configuração WSGI
│   ├── asgi.py               # Configuração ASGI
│   ├── database_router.py    # Router para múltiplos bancos
│   ├── utils/                # Utilitários
│   │    ├── __init__.py
│   │    ├── pipeline.py       # Pipeline base para processamento de dados
│   │    └── paginators.py     # Classe para fazer paginação de querys.
├── dw_analytics/              # App de análise do Data Warehouse
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├──  0001_initial.py
│   │   ├──  0002_fincidentsbita_updated_at.py
│   │   ├──  0004_remove_fincidentsbita_updated_at.py
│   │   ├──  0004_remove_fincidentsbita_updated_at.py
│   │   ├──  0005_alter_fincidentsbita_id.py
│   │   ├──  0006_fincidentsbita_updated_at_alter_fincidentsbita_id.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── d_assignment_group.py
│   │   ├── d_company.py
│   │   ├── d_contract.py
│   │   ├── d_operacao.py
│   │   ├── d_premissas.py
│   │   ├── d_resolved_by.py
│   │   ├── d_resolved_by_assignment_group.py
│   │   ├── d_sorted_ticket.py
│   │   ├── f_incident.py
│   │   ├── f_incident_bita.py
│   │   ├── f_incident_task.py
│   │   ├── f_planta_vgr.py
│   │   └── f_sae_localidades.py
│   ├── api/
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── f_incidents_bita_serizalizer.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   └── f_incidents_bita_viewset.py
│   │   └── urls.py
├── power_bi/                  # App de integração com Power BI
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_rename_municýpio_tblsolarinterfacesvgr_municipio.py
│   │   ├── 0003_alter_tblsolarinterfacesvgr_municipio.py
│   │   ├── 0004_solaridvgrinterfacecorrigido.py
│   │   ├── 0005_alter_solaridvgrinterfacecorrigido_company_remedy_and_more.py
│   │   ├── 0006_solaridvgrinterfacecorrigido_historico_ids.py
│   │   ├── 0007_alter_solaridvgrinterfacecorrigido_historico_ids.py
│   │   └── 0008_alter_solaridvgrinterfacecorrigido_velocidade.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── demais_models.py
│   │   ├── solaridvgrinterfacecorrigido.py
│   │   └── tblsolarinterfacesvgr.py
│   ├── api/
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   └── solar_new_id_serializer.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── solar_id_vgr_interface_vgr_corrigido_viewset.py
│   │   │   ├── solar_interfaces_vgr.py
│   │   │   └── load_interfaces_new_id.py
│   │   └── urls.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── load_interface_new_id.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mixin.py
└── manage.py                 # Script de gerenciamento Django
```

## Configuração do Ambiente

1. Clone o repositório
2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (.env)
```env
DB_NAME_APLICATION=nome_banco
DB_NAME_DW_ANALYTICS=nome_dw
DB_NAME_POWER_BI=nome_powerbi
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=servidor
DB_PORT=1433
DB_DRIVER=SQL Server Native Client 11.0
```

5. Execute as migrações
```bash
python manage.py migrate
```

## Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O servidor backend estará disponível em `http://localhost:8000/`
