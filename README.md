# py-json-server
## Overview
This application allows you to create GET API from directory with yaml files. <br>
The endpoints are build based on directory structure.  <br>
The server allows some yaml preprocessing before serving to endpoints. <br> 
You can enable bearer token authentication based on JWT tokens. <br>
This is fastapi based so you get automatically generated opeanapi.json served under `/docs`.

## Developing
### Local setup without docker
For app to work properly you need python3.8+ <br>
Install requirements and ASGI server of your choice. 
I develop with `uvicorn` and Dockerfile is `gunicorn` based.

```
pip install -r requirements.txt
pip install uvicorn[standard]
# start app with default ip, port
uvicorn --reload app.main:app
```
## Building
You can build dockerfile manually based on provided `Dockerfile`
```
docker build . -t py-json-server
```

## Check generated API
After running app enter `${APP_ADDRESS}/docs`.

## Running as docker container
If you built docker image from Dockerfile or pulled from docker repo.
Run http server on port 8080 and publish to host on the same port.
```
docker run -p 8080:8080 python-json:latest --host 0.0.0.0 --port 8080
```

## Configuration
List of available settings:
