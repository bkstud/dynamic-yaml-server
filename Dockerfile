FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apk update && apk add gcc libc-dev

RUN pip3 install -r requirements.txt

RUN pip3 install uvicorn[standard]

COPY . .

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]
