FROM python:3.8-alpine as base
FROM base as builder

WORKDIR /install
COPY requirements.txt requirements.txt
RUN apk update && apk add gcc libc-dev
RUN pip3 install --prefix=/install -r requirements.txt
RUN pip3 install --prefix=/install uvicorn[standard]


FROM base

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .

ENTRYPOINT ["uvicorn", "app.main:app"]
