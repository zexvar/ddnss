#! /bin/bash
# gunicorn -b [::]:5000 run:app &
# shellcheck disable=SC2101
nohup gunicorn -b [::]:5000 run:app > out.log 2>&1 &