from fastapi.security import APIKeyHeader
from starlette.authentication import \
    AuthenticationBackend as AuthenticationInterface
from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection

from app.auth.jwt import validate


class AuthenticationBackend(AuthenticationInterface):
    """
    Own Auth Backend based on Starlette's AuthenticationBackend.

    Use instance of this class as `backend` argument to `add_middleware` func:

    .. code-block:: python

        app = FastAPI()

        @app.on_event('startup')
        async def startup():
            app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

    """
    async def authenticate(
        self, conn: HTTPConnection,
    ):
        token_header = APIKeyHeader(name="token", auto_error=False)
        token = await token_header(conn)
        if not token:
            raise AuthenticationError("Token missing")
        validate(token)
        return True
