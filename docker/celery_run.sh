#!/bin/bash

if $CELERY_RUN ; then
    rm -rf /code/badpanty/*.pid
    celery -A app.tasks.celery:celery beat --loglevel=info & \
    celery -A app.tasks.celery:celery worker --loglevel=info -B
fi
