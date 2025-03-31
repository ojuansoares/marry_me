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

---

## Product Backlog

| ID | Item                                                                |
| -- | ------------------------------------------------------------------- |
| 1  | Criar conta e configurar perfil do casamento                        |
| 2  | Criar e personalizar lista de convidados                            |
| 3  | Categorizar convidados por tipo (familiares, amigos, colegas, etc.) |
| 4  | Gerar QR code único para cada convidado                             |
| 5  | Compartilhar informações do evento com convidados                   |
| 6  | Criar galeria de fotos para os convidados deixarem mensagens        |
| 7  | Criar e gerenciar lista de presentes                                |
| 8  | Acompanhar confirmações de presença e presentes reservados          |
| 9  | Criar funcionalidade de chat entre noivos e convidados              |
| 10 | Permitir atualização de informações do evento                       |
| 11 | Integrar câmera do dispositivo para compartilhamento de fotos       |
| 12 | Adicionar contagem regressiva para o dia do casamento               |
| 13 | Criar funcionalidade para upload de fotos dos convidados            |
| 14 | Criar lembretes para prazos importantes                             |
| 15 | Criar planilha de orçamento e alertas de gastos                     |
| 16 | Integrar GPS para localização do evento                             |
| 17 | Criar notificações personalizadas                                   |
| 18 | Exibir estatísticas sobre a interação dos convidados                |
| 19 | Criar seção para visualizar fotos enviadas pelos convidados         |
| 20 | Enviar mensagens de agradecimento personalizadas após o evento      |

---

## Sprint Backlog

### SPRINT 1:

| ID | Item                                                       |
| -- | ---------------------------------------------------------- |
| 1  | Criar conta e configurar perfil do casamento               |
| 2  | Criar e personalizar lista de convidados                   |
| 3  | Criar categoria de convidados                              |
| 5  | Compartilhar informações do evento com convidados          |
| 6  | Criar galeria de fotos com mensagens                       |
| 7  | Criar e gerenciar lista de presentes                       |
| 8  | Acompanhar confirmações de presença e presentes reservados |
| 10 | Permitir atualização de informações do evento              |

### SPRINT 2:

| ID | Item                                                  |
| -- | ----------------------------------------------------- |
| 12 | Criar funcionalidade de contagem regressiva           |
| 18 | Exibir estatísticas de interação dos convidados       |
| 21 | Gerar planilha com presença e detalhes dos convidados |
| 14 | Criar lembretes para prazos importantes               |
| 16 | Integrar GPS para localização do evento               |
| 17 | Criar notificações personalizadas                     |

### SPRINT 3:

| ID | Item                                                     |
| -- | -------------------------------------------------------- |
| 15 | Criar planilha de orçamento com alertas de gastos        |
| 9  | Criar funcionalidade de chat entre noivos e convidados   |
| 20 | Enviar mensagens de agradecimento personalizadas         |
| 11 | Integrar câmera para compartilhamento de fotos           |
| 4  | Gerar QR code para registro de presença                  |
| 13 | Criar funcionalidade para upload de fotos dos convidados |
| 19 | Criar seção para visualizar fotos dos convidados         |

## Modelo Entidade-Relacionamento (MER)

Abaixo está o diagrama MER representando a estrutura do banco de dados:

![Diagrama MER](docs/mer.png)