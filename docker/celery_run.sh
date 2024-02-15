#!/bin/sh -ex

if $CELERY_RUN ; then
    celery -A app.tasks.celery:celery beat --loglevel=debug &
    celery -A app.tasks.celery:celery worker --loglevel=info &
    tail -f /dev/null
fi
