FROM python:slim-bullseye
WORKDIR ./DDNS_Cloudflare
ADD . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "[::]:5000", "run:app"]
