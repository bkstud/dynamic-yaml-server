"Json web token related functions"
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.common.utils import logger
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_user_from_bearer(token: str = Depends(oauth2_scheme)) -> str:
    """Validates and decodes token and extracts user from it.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.secret_key,
                             algorithms=[settings.jwt_algorithm])
        username: Optional[str] = payload.get("sub")
        if username is None:
            logger.warning(f"Failed bearer auth try with token '{token}'")
            raise credentials_exception
    except JWTError as jwt_error:
        logger.warning(f"Failed bearer auth token try with '{token}'. "
                       f"JWTError: {jwt_error}")
        raise credentials_exception from jwt_error
    return username


def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None,
                        key=settings.secret_key):
    "Creates new signed jwt token with encoded data"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + \
                 timedelta(minutes=settings.jwt_token_exipre)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=settings.jwt_algorithm)
    return encoded_jwt
