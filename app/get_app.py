from fastapi import Depends, FastAPI

from .auth.login import login_for_access_token
from .auth.authorize import get_user_from_bearer
from .config import settings
from .router.dynamic import DynamicJsonRouter


def get_app():
    app = FastAPI(title=settings.app_title)

    if settings.server_mode == "dynamic":
        router = DynamicJsonRouter(settings.share_content_input_dir)
        dependencies = []
        if settings.auth_method.lower() == "jwt":
            app.add_api_route("/login",
                              login_for_access_token, methods=["POST"])
            dependencies.append(Depends(get_user_from_bearer))
        app.include_router(router, prefix=settings.api_endpoint_begin,
                           dependencies=dependencies)
    return app
