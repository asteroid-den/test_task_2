from fastapi import FastAPI
from fastapi.middleware import Middleware

from config import Config
from middlewares import DatabaseMiddleware
from routers import multicheque_info
from services.database import DatabaseManager

config = Config()

database_manager = DatabaseManager(
    user=config.db_user,
    password=config.db_password,
    host=config.db_host,
    db_name=config.db_name,
)

middleware = [Middleware(DatabaseMiddleware, database_manager=database_manager)]

app = FastAPI(middleware=middleware)

app.include_router(router=multicheque_info.router)
