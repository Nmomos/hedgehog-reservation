FROM python:3.9-alpine

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /backend/requirements.txt

RUN set -eux \
 && apk add --no-cache build-base \
 && pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r /backend/requirements.txt \
 && apk del build-base \
 && rm -rf /root/.cache/pip

COPY . /backend
