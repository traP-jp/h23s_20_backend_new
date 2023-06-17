FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add  --no-cache build-base

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]