FROM python:3.9.2-alpine3.13

LABEL maintainer="nmrkthilakraj@gmail.com"

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del --no-cache .build-deps && apk add postgresql-libs
COPY . .

CMD [ "./docker-entrypoint.sh" ]
