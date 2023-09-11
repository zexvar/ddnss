#!/usr/bin/env bash


# gunicorn main:app \
#   --workers=2 \
#   --worker-class=gevent \
#   --worker-connections=2000 \
#   --bind [::]:5000

gunicorn -w 2 -k gevent -b [::]:5000 main:app