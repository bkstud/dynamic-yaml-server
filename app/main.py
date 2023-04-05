from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth.backend import AuthenticationBackend
from .auth.middleware import AuthenticationMiddleware
from .auth.jwt import create_access_token
from .common.shareable import prepare_json_contents
from .config import settings
from .router.dynamic import DynamicJsonRouter
from .common.utils import logger


app = FastAPI()


app.add_middleware(AuthenticationMiddleware, backend=AuthenticationBackend())



if settings.server_mode == "dynamic":
    router = DynamicJsonRouter(settings.share_content_input_dir)
    app.include_router(router, prefix="/share")
elif settings.server_mode == "static":
    prepare_json_contents(
        settings.share_content_input_dir,
        settings.share_content_output_dir)
    static_files_app = StaticFiles(directory=settings.share_content_output_dir)
    app.mount("/share", static_files_app, name="static")


# # TODO:  /login -> duobackend,someegenerated_password -> jwttoken
# TODO: Probably this example token should go to file specified in setting
# Also secret used to sign jwt could go to separate file so that it possibly
# could be accessed
logger.info(f"Authorization: Bearer {create_access_token({})}")


# # for testing wrong key
# print(create_access_token({},
#       key="19d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"))
