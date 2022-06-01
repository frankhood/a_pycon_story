#!/usr/bin/env bash

trap cleanup SIGINT SIGTERM

SLEEP_AFTER_CRASH=${SLEEP_AFTER_CRASH:-5}

cleanup () {
    echo "SIGTERM"
    kill -s SIGTERM $!
    exit 0
}

start () {
    # pip-sync requirements/dev.txt --pip-args "--src /root/src"
    # python manage.py migrate --noinput
    echo "QCLUSTER_WATCH_RESTART"
    echo ${QCLUSTER_WATCH_RESTART}
    if [[ -z "${QCLUSTER_WATCH_RESTART}" ]]; then
        base_start
    else
        reload_start
    fi
}

base_start() {
    echo "MONITORING OFF!"
    while true; do
        python manage.py qcluster
        wait $!
        sleep $SLEEP_AFTER_CRASH
    done
}

reload_start() {
    echo "MONITORING ON!"
    while true; do
        python manage.py qcluster &
        DO_WATCH=true
        while $DO_WATCH; do
            # Monitor change in /app folder (only .py file)
            filename=$(inotifywait --quiet -e modify -e move -e create -e delete -e attrib --format "%f" -r /app)
            [[ $filename == *.py ]] && DO_WATCH=false
            [[ $filename == *.env ]] && DO_WATCH=false
        done
        # gracefully restart of qcluster
        pkill -e -2 --full 'python manage.py qcluster'
        wait $!
        sleep $SLEEP_AFTER_CRASH
    done
}

start
