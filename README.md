# Casamento App

Um aplicativo para gerenciamento de casamentos, desenvolvido com React Native (Expo) no frontend e FastAPI + PostgreSQL no backend.

## Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── crud/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── utils/
│   ├── requirements.txt
│   └── .env
└── frontend/
    └── (React Native/Expo files will be here)
```

## Backend Setup

1. Crie um ambiente virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure o arquivo .env:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Configure o banco de dados PostgreSQL:
- Crie um banco de dados chamado 'casamento'
- As tabelas serão criadas automaticamente ao iniciar a aplicação

5. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

O backend estará disponível em `http://localhost:8000`

## Frontend Setup (Em breve)

O frontend será desenvolvido com React Native usando Expo.

## API Documentation

Após iniciar o servidor, a documentação da API estará disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Funcionalidades Principais

- Gerenciamento de usuários (noivos e convidados)
- Gerenciamento de casamentos
- Sistema de convites e confirmações
- Grupos de convidados
- Sistema de lembretes
- Galeria de fotos
- Controle de orçamento

## Tecnologias Utilizadas

Backend:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication

Frontend (Em breve):
- React Native
- Expo
- React Navigation
- Axios
- AsyncStorage 