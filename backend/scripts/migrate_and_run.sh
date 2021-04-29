#!/bin/bash
set -e # fail on errors

`dirname $0`/wait_for_services.sh
./manage.py  migrate
./manage.py init_db
python3 -m infinity_meme.bot