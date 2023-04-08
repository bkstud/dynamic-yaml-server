from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.config import settings
from app.common.utils import logger

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
        username: str = payload.get("sub")
        if username is None:
            logger.warning(f"Failed bearer auth try with token '{token}'")
            raise credentials_exception
    except JWTError as jwt_error:
        logger.warning(f"Failed bearer auth token try with '{token}'. "
                       f"JWTError: {jwt_error}")
        raise credentials_exception
    return username
