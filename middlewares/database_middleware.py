from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from services.database import DAO, DatabaseManager


class DatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, database_manager: DatabaseManager):
        super().__init__(app)
        self.database_manager = database_manager

    async def dispatch(self, request: Request, call_next) -> Response:
        dao = DAO(session=self.database_manager.session())
        request.state.dao = dao

        return await call_next(request)

        await dao.close()

