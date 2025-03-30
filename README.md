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
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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

Para rodar o projeto, você pode usar:

```bash
npx expo start
```

Isso vai iniciar o servidor de desenvolvimento do Expo e mostrar um QR code. Você tem algumas opções para rodar o app:

1. **No celular físico**:
   - Instale o aplicativo "Expo Go" no seu celular (disponível na Play Store ou App Store)
   - Escaneie o QR code que aparece no terminal com o app Expo Go
   - O app vai carregar automaticamente no seu celular

2. **No emulador Android**:
   - Tenha o Android Studio instalado com um emulador configurado
   - Pressione 'a' no terminal onde o Expo está rodando para abrir no emulador Android

3. **No simulador iOS** (apenas para usuários Mac):
   - Tenha o Xcode instalado
   - Pressione 'i' no terminal onde o Expo está rodando para abrir no simulador iOS 