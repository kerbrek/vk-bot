#!/bin/bash

./wait-for-it.sh "${POSTGRES_HOST}:${POSTGRES_PORT}"
echo Initializing database...
python fill_db_with_sample_data.py

echo Starting application...
exec "$@"
