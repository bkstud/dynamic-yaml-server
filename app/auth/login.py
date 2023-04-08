from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import settings

from .jwt import create_access_token


def authenticate_user(username: str, password: str):
    if not username or username != settings.default_user:
        return False
    if not password == settings.default_password:
        return False
    return username


async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user})
    return {"access_token": access_token, "token_type": "bearer"}
