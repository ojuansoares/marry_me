from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import define_routers
from app.core.database import Base, engine
from app.models.models import (
    User,
    Wedding,
    Guest,
    Reminder,
    Image,
    Budget,
    usertype,
    weddingstatus,
    phototype
)
from sqlalchemy import text
import os

app = FastAPI(
    title="Wedding API",
    description="API for wedding management",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("Initializing database connection...")

    # Executa comandos SQL que precisam de AUTOCOMMIT (como DO $$)
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text("SET search_path TO public"))

        # Criação segura dos ENUMs se ainda não existirem
        conn.execute(text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'usertype') THEN
                CREATE TYPE public.usertype AS ENUM ('fiance', 'guest');
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'weddingstatus') THEN
                CREATE TYPE public.weddingstatus AS ENUM ('active', 'postponed', 'cancelled');
            END IF;

            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'phototype') THEN
                CREATE TYPE public.phototype AS ENUM ('couple', 'guests');
            END IF;
        END;
        $$;
        """))

    # Só agora criamos as tabelas (depois dos ENUMs existirem!)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

define_routers(app)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Wedding API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 