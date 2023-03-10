from datetime import datetime, timedelta
from typing import Union

from jose import JWTError, jwt
from starlette.authentication import AuthenticationError


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def validate(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY)
    except JWTError as jwt_err:
        raise AuthenticationError(str(jwt_err))
    return True


def create_access_token(data: dict,
                        expires_delta: Union[timedelta, None] = None,
                        key=SECRET_KEY):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + \
                 timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=ALGORITHM)
    return encoded_jwt
