#! /bin/bash
# gunicorn -b [::]:5000 run:app &
# shellcheck disable=SC2101
nohup gunicorn run:app -c gunicorn.py > out.log 2>&1 &