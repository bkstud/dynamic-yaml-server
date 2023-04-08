FROM python:3.8-alpine as base
FROM base as builder

WORKDIR /install
COPY requirements.txt requirements.txt
RUN apk update && apk add gcc libc-dev
RUN pip3 install --prefix=/install -r requirements.txt
RUN pip3 install --prefix=/install gunicorn==20.1.0


FROM base

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
CMD ["gunicorn", "--host", "0.0.0.0", "app.main:app"]
