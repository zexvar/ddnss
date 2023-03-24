#! /bin/bash
#nohup gunicorn main:app -w 2 -k gevent -b [::]:5000 >out.log 2>&1 &
gunicorn main:app -c main.py