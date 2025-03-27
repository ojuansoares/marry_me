# -*- encoding: utf-8 -*-

from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.routers.users import router as user_router

def define_routers(app: FastAPI) -> None:
    app.include_router(user_router)