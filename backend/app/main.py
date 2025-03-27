from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import define_routers
from app.core.config import settings
from app.core.database import Base, engine
from app.models.models import (
    Usuario,
    Casamento,
    GrupoConvidados,
    Convidado,
    Lembrete,
    Foto,
    Orcamento,
    usertype,
    weddingstatus,
    phototype
)
from sqlalchemy import text

app = FastAPI(
    title="Casamento API",
    description="API para gerenciamento de casamentos",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar tipos ENUM e tabelas do banco de dados
@app.on_event("startup")
async def startup_event():
    print("Criando tipos ENUM...")
    async with engine.connect() as conn:
        # Criar tipos ENUM se não existirem
        await conn.execute(text("DO $$ BEGIN CREATE TYPE usertype AS ENUM ('noivo', 'convidado'); EXCEPTION WHEN duplicate_object THEN null; END $$;"))
        await conn.execute(text("DO $$ BEGIN CREATE TYPE weddingstatus AS ENUM ('ativo', 'adiado', 'cancelado'); EXCEPTION WHEN duplicate_object THEN null; END $$;"))
        await conn.execute(text("DO $$ BEGIN CREATE TYPE phototype AS ENUM ('noivos', 'convidados'); EXCEPTION WHEN duplicate_object THEN null; END $$;"))
        await conn.commit()
    
    print("Criando tabelas do banco de dados...")
    async with engine.connect() as conn:
        await conn.execute(text("SET search_path TO public"))
        await conn.run_sync(Base.metadata.create_all)
    print("Tabelas criadas com sucesso!")

define_routers(app)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API de Casamento",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 