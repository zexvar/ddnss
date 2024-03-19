#!/bin/sh

# gunicorn run
gunicorn main:app \
--workers 2 \
--worker-class=gevent \
--worker-connections 1024 \
--bind [::]:5533

exec "$@"