#!/bin/bash
set -e # fail on errors

gunicorn --bind='0.0.0.0:8000' --workers=4 --forwarded-allow-ips='*' django_backend.wsgi:application
