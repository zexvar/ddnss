#! /bin/bash
# nohup gunicorn -w 2 -b [::]:5000 main:app  >out.log 2>&1 &
# nohup gunicorn -w 2 -k gevent -b [::]:5000 main:app  >out.log 2>&1 &

gunicorn main:app \
  --workers=2 \
  --worker_class=gevent \
  --worker_connections=2000 \
  --bind [::]:5000
