FROM python:alpine
WORKDIR /ddnss
ADD src .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
CMD ["sh", "init.sh"]