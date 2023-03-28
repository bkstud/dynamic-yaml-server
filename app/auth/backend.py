from fastapi.security import APIKeyHeader
from starlette.authentication import \
    AuthenticationBackend as AuthenticationInterface
from starlette.authentication import AuthenticationError
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import HTTPConnection
from app.auth.jwt import validate as jwt_validate
from app.config import settings


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
        auth_header = APIKeyHeader(name="Authorization", auto_error=False)
        header = await auth_header(conn)
        if not header:
            raise AuthenticationError("Missing authorization header.")
        scheme, creds = get_authorization_scheme_param(header)
        if not scheme:
            raise AuthenticationError("Missing authentication scheme.")
        if not creds:
            raise AuthenticationError("Mising authentication credentials.")
        if scheme != "Bearer":
            raise AuthenticationError("Only bearer authorizaton supported.")
        validator = jwt_validate
        
        if settings.auth_method == "jwt":
            validator = jwt_validate
        else:
            raise NotImplementedError()

        return validator(creds)
