FROM python:slim-bullseye
WORKDIR ./opt/ddns
ADD src .
RUN apt update && apt install -y vim && apt clean -y
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN chmod +x init.sh
CMD ["./init.sh"]
