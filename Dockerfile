FROM python:3.10

LABEL maintainer="vsevolod.doronin@yandex.ru"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./alembic.ini /code/alembic.ini
COPY ./migrations /code/migrations

# Устанавливаем зависемости
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt