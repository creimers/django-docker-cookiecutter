#!/bin/sh

python /project/manage.py collectstatic --noinput
python /project/manage.py migrate --noinput
/usr/local/bin/gunicorn wsgi -w 5 --bind 0.0.0.0:8000 --chdir=/project --access-logfile - --access-logformat "%(h)s %(t)s %(s)s %(U)s %(L)s"
