# Sistema Base Django + React

## 📋 Sobre o Projeto

Projeto base desenvolvido com Django e React, fornecendo uma estrutura inicial com sistema de autenticação completo. Ideal para iniciar novos projetos que necessitem de um sistema de login já configurado e funcional.

## 🎯 Funcionalidades Implementadas

- Sistema de autenticação completo
- Login e registro de usuários
- Proteção de rotas no frontend
- Autenticação via tokens JWT
- Estrutura base do projeto Django
- Interface base em React

## 🛠️ Tecnologias Utilizadas

### Frontend
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Material-UI](https://img.shields.io/badge/Material--UI-0081CB?style=for-the-badge&logo=material-ui&logoColor=white)](https://mui.com/)
[![Axios](https://img.shields.io/badge/Axios-671DDF?style=for-the-badge&logo=axios&logoColor=white)](https://axios-http.com/)

### Backend
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io/)

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.8 ou superior
- Node.js versão 18 ou superior
- npm ou yarn

### Backend

1. Criar ambiente virtual Python
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependências
```bash
pip install -r requirements.txt
```

3. Executar migrações
```bash
python manage.py migrate
```

4. Iniciar servidor
```bash
python manage.py runserver
```

### Frontend

1. Instalar dependências
```bash
cd frontend
npm install
```

2. Iniciar servidor de desenvolvimento
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`
O backend estará disponível em `http://localhost:8000`

## 📊 Estrutura do Projeto

### Backend
- Autenticação JWT configurada
- Django REST Framework setup
- CORS configurado
- Endpoints de autenticação prontos
- Swagger/OpenAPI documentação

### Frontend
- Sistema de rotas configurado
- Contexto de autenticação
- Interceptors do Axios
- Páginas de login/registro
- Layout base responsivo

## 🤝 Contribuindo

1. Faça o fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

---
