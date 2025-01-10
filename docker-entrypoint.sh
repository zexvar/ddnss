#!/bin/sh

# waitress serve
exec waitress-serve \
--listen *:5533 \
"$@" \
app:app