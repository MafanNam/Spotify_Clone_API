# pull official base image
FROM python:3.11-alpine3.15 as builder
LABEL maintainer="Mafan"

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements/local.txt /app/local.txt
COPY ./requirements/base.txt /app/base.txt

RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install -r local.txt

COPY . /app
COPY ./.envs /app/.envs
COPY ./docker/local /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh
RUN chmod +x /app/docker/backend/celery-beat-entrypoint.sh
