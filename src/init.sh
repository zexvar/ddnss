#!/usr/bin/env sh


# gunicorn main:app --workers=2 --worker-class=gevent --bind [::]:5000
gunicorn main:app -w 2 -k gevent -b [::]:5000