# -*- encoding: utf-8 -*-

from fastapi import FastAPI
from app.routers import users

def define_routers(app: FastAPI) -> None:
    app.include_router(users.router)
