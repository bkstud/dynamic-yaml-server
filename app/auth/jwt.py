from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt
from starlette.authentication import AuthenticationError, SimpleUser

from app.config import settings


def validate(token: str) -> bool:
    decoded = None
    try:
        decoded = jwt.decode(token,
                             settings.secret_key,
                             algorithms=settings.jwt_algorithm)
    except JWTError as jwt_err:
        raise AuthenticationError(str(jwt_err))
    user = SimpleUser(decoded.get("user", "jwt token"))
    return decoded, user


def create_access_token(data: dict,
                        expires_delta: Union[timedelta, None] = None,
                        key=settings.secret_key):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + \
                 timedelta(minutes=settings.jwt_token_exipre)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=settings.jwt_algorithm)
    return encoded_jwt
