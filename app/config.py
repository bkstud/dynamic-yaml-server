import os
from pathlib import Path

from pydantic import BaseSettings
from typing import Optional
from app.auth.utils import default_token_generator

app_secrets_dir: Optional[str] = os.environ.get(
    "APP_SECRETS_DIR", "/run/secrets"
)
if not Path(app_secrets_dir).exists():
    config_secrets_dir = None


class Settings(BaseSettings):
    """
    Configuration settings for this library.

    For now you could only change the settings
    via APP_<ATTRIBUTE_NAME> environment variables.
    # TODO Update docs with current style
    :param logger: Dotted path to the logger (using this attribute, standard
                   logging methods will be used: logging.debug(), .info(), etc.
    :param log_level: Standard LEVEL for logging (DEBUG/INFO/WARNING/etc.)
    """
    logger: str = "logging"
    log_level: str = "INFO"
    service_name: str = "json_server"

    secret_key: str = default_token_generator()

    # TODO: Lets make auth method for now to have 2 options
    # one is jwt token based, second will be single token comparison
    auth_method: str = "jwt"
    jwt_algorithm: str = "HS256"
    jwt_token_exipre: int = 30

    share_content_input_dir: str = "./static"
    share_content_output_dir: str = "./share"

    # server mode can be static or dynamic
    server_mode: str = "dynamic"

    key_name: str = ""

    fastapi_app: str = None  # e.g. "project.server.app", where app = FastAPI()

    class Config:
        env_prefix = "APP_"
        secrets_dir = config_secrets_dir


settings = Settings()
