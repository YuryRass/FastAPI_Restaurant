#!/bin/bash

if [[ "${MODE}" == "DEV" ]]; then
    alembic upgrade head
    uvicorn app.main:app --host=0.0.0.0
elif [[ "${MODE}" == "TEST" ]]; then
    python3 -m pytest ./app/tests/test_menu.py -v
fi
