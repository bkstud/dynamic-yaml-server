"""End to end tests for app"""

import json
import os
import tempfile

from fastapi.testclient import TestClient

from .config import Settings, settings
from .get_app import get_app


def make_client():
    return TestClient(get_app())


def login_client(client,
                 username=settings.default_user,
                 password=settings.default_password):
    data = {
            "username": username,
            "password": password
        }
    return client.post("/login", data=data)


def test_not_found():
    client = make_client()
    response = client.get("/asdf")
    assert response.status_code == 404


def test_default_login():
    client = make_client()
    response = login_client(client)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


def test_login_wrong_user():
    client = make_client()
    response = login_client(client, username="wrong")
    assert response.status_code == 401


def test_login_wrong_password():
    client = make_client()
    response = login_client(client, password="wrong")
    assert response.status_code == 401


def test_get_content():
    json_content = """[
        {"id": 1},
        {"id": 2}
    ]"""
    json_content = json_content.replace("\n", "").replace(" ", "")
    with tempfile.TemporaryDirectory(dir=".") as tmpdirname:
        with open(os.path.join(tmpdirname, "content.json"), "w") as jsonfile:
            jsonfile.write(json_content)
        settings.share_content_input_dir = tmpdirname
        settings.api_endpoint_begin = "/test"
        client_ = make_client()
        bearer = login_client(client_).json()["access_token"]

    content = client_.get("/test/content",
                          headers={"Authorization": f"Bearer {bearer}"})
    settings.api_endpoint_begin = Settings().api_endpoint_begin
    assert content.status_code == 200, \
           json.loads(json_content) == content.json()


def test_get_openapi_schema():
    assert make_client().get("/openapi.json").status_code == 200


def test_get_broken_json_no_comma():
    json_file_broken = '''[
        {"id": 1}
        {"id": 2}
    ]'''
    with tempfile.TemporaryDirectory(dir=".") as tmpdirname:
        with open(os.path.join(tmpdirname, "broken.json"), "w") as jsonfile:
            jsonfile.write(json_file_broken)
        settings.share_content_input_dir = tmpdirname
        client_ = make_client()

        bearer = login_client(client_).json()["access_token"]
        response = client_.get(f"{settings.api_endpoint_begin}/broken",
                               headers={"Authorization": f"Bearer {bearer}"})

        json_resp = response.json()
        assert response.status_code == 500
        assert "Expecting ',' delimiter" in json_resp["error"]
        assert "broken.json is not valid json" in json_resp["detail"]
