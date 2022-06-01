#!/usr/bin/env bash

trap cleanup SIGINT SIGTERM

EXPOSE_PORT=${EXPOSE_PORT:-8030}
SLEEP_AFTER_CRASH=${SLEEP_AFTER_CRASH:-5}

cleanup () {
    echo "SIGTERM"
    kill -s SIGTERM $!
    exit 0
}

start () {
    pip-sync requirements/dev.txt --pip-args "--src /root/src"
    pre-commit install || true
    python manage.py migrate --noinput
    if [ ! -f /app/docker.code-workspace ]
    then
        cp /app/docker/docker.code-workspace.tmpl /app/docker.code-workspace
    fi

    while true; do
        python manage.py runserver 0.0.0.0:$EXPOSE_PORT
        wait $!
        sleep $SLEEP_AFTER_CRASH
    done
}

start
