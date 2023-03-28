from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth.backend import AuthenticationBackend
from .auth.middleware import AuthenticationMiddleware
from .auth.jwt import create_access_token
from .common.shareable import prepare_json_contents
from .config import settings

print(settings.secret_key)
app = FastAPI()

prepare_json_contents(
    settings.share_content_input_dir,
    settings.share_content_output_dir)

app.add_middleware(AuthenticationMiddleware, backend=AuthenticationBackend())


static_files_app = StaticFiles(directory="share", follow_symlink=True)
app.mount("/share", static_files_app, name="static")

print(create_access_token({}))

# # for testing wrong key
# print(create_access_token({},
#       key="19d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"))
