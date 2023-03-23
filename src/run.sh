#! /bin/bash
# gunicorn -b [::]:5000 run:app &
# shellcheck disable=SC2101
nohup gunicorn run:app \
  -b [::]:5000 \
  -w 4 \
  -k gevent \
  >out.log 2>&1 &
