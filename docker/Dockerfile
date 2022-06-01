FROM python:3.8-slim-buster AS base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        gettext \
        libpq5 \
        mime-support \
        libmariadb-dev-compat \
        gcc \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app


FROM base AS prodDocker

COPY ./requirements/prod.txt requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        libpq-dev \
        libmariadb-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --clear --noinput && \
    uwsgi uwsgiconf/docker.ini


FROM base AS start_dev

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        libpq-dev \
        make \
        ssh-client \
        libmariadb-dev-compat \
        libmariadb-dev \
        libssl-dev \ 
        libffi-dev
RUN apt-get install -y --no-install-recommends  \
        inotify-tools  \
        procps
SHELL ["/bin/bash", "-c"]
WORKDIR /root
RUN git clone --depth 1 --config core.autocrlf=false https://github.com/twolfson/sexy-bash-prompt 
RUN cd sexy-bash-prompt && make install
WORKDIR /app

FROM start_dev AS dev

COPY ./requirements/dev.txt requirements.txt
RUN pip install --no-cache-dir --src /root/src -r requirements.txt
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --clear --noinput

FROM base AS test

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libmariadb-dev \
    && pip install --no-cache-dir --src /root/src -U pip tox
CMD tox -e coverage,reporthtml,report
