FROM python:slim-bullseye
WORKDIR ./opt/ddns
ADD src .
RUN apt update && apt install -y vim && apt clean -y
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
CMD ["gunicorn", "main:app", "-c", "main.py"]
