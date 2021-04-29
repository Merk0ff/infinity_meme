#!/bin/bash

set -e # fail on errors

# wait for Postgres to start
function postgres_ready(){
python3 << END
import os
import sys
import psycopg2
from envparse import env
try:
    conn = psycopg2.connect(
        dbname=env.str('DB_NAME'),
        user=env.str('DB_USER'),
        password=env.str('DB_PASSWORD'),
        host=env.str('DB_HOST'),
        port=env.int('DB_PORT'),
        connect_timeout=3,
    )
except psycopg2.OperationalError as e:
    sys.exit(-1)
sys.exit(0)
END
}


until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
