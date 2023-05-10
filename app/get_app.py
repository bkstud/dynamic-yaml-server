from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from .auth.backend import AuthenticationBackend
from .auth.login import login_for_access_token
from .auth.authorize import get_user_from_bearer
from .auth.middleware import AuthenticationMiddleware
from .config import settings
from .router.dynamic import DynamicJsonRouter
from .common.shareable import prepare_json_contents


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
    elif settings.server_mode == "static":
        app.add_middleware(AuthenticationMiddleware,
                           backend=AuthenticationBackend())
        prepare_json_contents(
            settings.share_content_input_dir,
            settings.share_content_output_dir)
        static_files_app = StaticFiles(
            directory=settings.share_content_output_dir)
        app.mount("/share", static_files_app, name="static")

    return app