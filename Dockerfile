FROM python:3.8-alpine as base
FROM base as builder

WORKDIR /install
COPY requirements.txt requirements.txt
RUN apk update && apk add gcc libc-dev
RUN pip3 install --prefix=/install -r requirements.txt

FROM base

WORKDIR /
COPY --from=builder /install /usr/local
COPY /app /app

ENTRYPOINT ["uvicorn", "app.main:app"]
