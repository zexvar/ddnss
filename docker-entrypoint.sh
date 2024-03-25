#!/bin/sh

# waitress run
waitress-serve \
--listen *:5533 \
--connection-limit 1024 \
"$@" \
app:app

exec "$@"