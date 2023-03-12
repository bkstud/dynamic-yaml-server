from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .auth.backend import AuthenticationBackend
from .auth.jwt import create_access_token
from .auth.middleware import AuthenticationMiddleware

app = FastAPI()
from .common.json import process_json

print(process_json("static/menu.json", "test.json"))

app.add_middleware(AuthenticationMiddleware, backend=AuthenticationBackend())

static_files_app = StaticFiles(directory="static")
app.mount("/static", static_files_app, name="static")

# print(create_access_token({}))
# # for testing wrong key
# print(create_access_token({},
#       key="19d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"))
