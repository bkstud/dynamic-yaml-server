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

    :param logger: Dotted path to the logger (using this attribute, standard
                   logging methods will be used: logging.debug(), .info(), etc.
    :param log_level: Standard LEVEL for logging (DEBUG/INFO/WARNING/etc.)
    """
    logger: str = "logging"
    log_level: str = "INFO"
    service_name: str = "json_server"
    secret_token: str = default_token_generator()

    fastapi_app: str = None  # e.g. "project.server.app", where app = FastAPI()

    class Config:
        env_prefix = "APP_"
        secrets_dir = config_secrets_dir


settings = Settings()
