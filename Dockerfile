FROM python:alpine
WORKDIR /ddnss
ADD src .
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN chmod +x init.sh
CMD ["./init.sh"]