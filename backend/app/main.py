from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import define_routers
from app.core.config import settings
from app.core.database import Base, engine
from app.models.models import (
    User,
    Wedding,
    GuestGroup,
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection and tables
@app.on_event("startup")
def startup_event():
    print("Initializing database connection...")
    
    # Set search path
    with engine.connect() as conn:
        conn.execute(text("SET search_path TO public"))
        
        # Execute init.sql if it exists
        init_sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'init.sql')
        if os.path.exists(init_sql_path):
            with open(init_sql_path, 'r') as f:
                init_sql = f.read()

            commands = [cmd.strip() for cmd in init_sql.split(';') if cmd.strip()]
            for command in commands:
                if command:
                    try:
                        conn.execute(text(command))
                    except Exception as e:
                        print(f"Error executing command: {str(e)}")
            
            conn.commit()

    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

# Include routers
define_routers(app)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Wedding API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 