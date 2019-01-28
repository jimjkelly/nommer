FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . /app
