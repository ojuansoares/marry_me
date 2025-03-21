from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import define_routers
from app.core.config import settings

app = FastAPI(
    title="Casamento API",
    description="API para gerenciamento de casamentos",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

define_routers(app)

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API de Casamento",
        "docs_url": "/api/v1/docs",
        "redoc_url": "/api/v1/redoc"
    } 