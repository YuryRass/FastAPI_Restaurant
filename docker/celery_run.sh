#!/bin/bash

if $CELERY_RUN ; then
    celery -A app.tasks.celery beat --loglevel=info & celery -A app.tasks.celery worker --loglevel=info -B
fi