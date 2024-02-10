FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /code/
