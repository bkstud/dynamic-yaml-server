"Conifg contains global settings class and instance"

import os
from typing import Optional

from pydantic import BaseSettings

from app.auth.utils import default_token_generator

app_secrets_dir: Optional[str] = os.environ.get(
    "APP_SECRETS_DIR", None
)


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """
    Configuration settings for this library.

    For now you could only change the settings
    via APP_<ATTRIBUTE_NAME> environment variables.

    Attributes:
        logger: logger to be used accross app.
        log_level: Standard LEVEL for logging (DEBUG/INFO/WARNING/etc.)
        secret_key: secret key to be used for JWT encoding/decoding.
        auth_method: authentication method currently can be JWT bearer.
                     or None for no auth check at all.
        jwt_algorithm: algorithm to be used for JWT
        jwt_token_expire: expiration time for jwt tokens
        api_endpoint_begin: Makes each contents endpoint to begin
                            with /api_endpoint_begin/...
        share_content_input_dir: Directory containing json
                                 files to be shared by server.
        default_user: Default user name for getting JWT token via /login.
        default_password: Default password for getting JWT token via /login.
        app_title: title name to be set for generated openapi name

        share_content_output_dir: For static server -
                                  currently not suported please ignore
    """
    logger: str = "loguru.logger"
    log_level: str = "INFO"
    app_title: str = "json_server"

    secret_key: str = default_token_generator()

    auth_method: str = "jwt"
    jwt_algorithm: str = "HS256"
    jwt_token_exipre: int = 30

    api_endpoint_begin: str = "/share"
    share_content_input_dir: str = "./static"

    # to be used in login to get jwt token
    default_user: str = "duo"
    default_password: str = "duo"

    share_content_output_dir: str = "./share"

    class Config:  # pylint: disable=too-few-public-methods
        "BaseSetting config class"
        env_prefix = "APP_"
        secrets_dir = app_secrets_dir


settings = Settings()
