# -*- encoding: utf-8 -*-

from fastapi import FastAPI, APIRouter
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.routers.users import get_router as get_users_router
from app.routers.weddings import router as wedding_router
from app.routers.auth import router as auth_router

def define_routers(app: FastAPI) -> None:
    app.include_router(get_users_router())
    app.include_router(wedding_router)
    app.include_router(auth_router)

def define_routers_api_router() -> APIRouter:
    router = APIRouter()
    
    # Include routers
    router.include_router(get_users_router())
    router.include_router(auth_router)
    
    return router
