FROM python:slim-bullseye
WORKDIR ./opt/ddns
ADD src .
RUN pip install -r requirement.txt
CMD ["gunicorn", "main:app", "-c", "main.py"]
