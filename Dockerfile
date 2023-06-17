FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache build-base libffi libffi-dev


RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]