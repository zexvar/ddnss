FROM python:slim-bullseye
WORKDIR ./opt/ddns
ADD . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "run:app", "-c", "gunicorn.py"]
