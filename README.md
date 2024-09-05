<div align=center>
   <img src="logo.png" width=50% alt="DDNS Server">
</div>

# Overview

DDNSS is an open-source DNS server used to simplify DNS services for multiple hosts. Clients do not need to install additional servers and can quickly update IP addresses through HTTP requests. The server directly obtains the source IP address of the request when receiving it

-Supports IPV4/IPV6 protocols
-Support rapid deployment of Docker images
-Developed using Flask framework based on Python language
-Update IP address through CloudFlare API

## Quickstart

### Server deploy

```shell
# build image
docker build https://github.com/zexvar/ddnss.git -t ddnss:latest
# from source code
git clone https://github.com/zexvar/ddnss
cd ddnss && docker compose up -d
```

### Client usage

- Basic
  ```shell
  curl -4 -L http://127.0.0.1:5533/dns/update/www/
  curl -6 -L http://[::1]:5533/dns/update/www/
  ```
- Wtih auth

  ```shell
  curl -4 -L http://<username>:<password>@<127.0.0.1>:5533/dns/update/www/
  curl -6 -L http://<username>:<password>@[::1]:5533/dns/update/www/
  ```

- With crontab

  ```shell
  */1 * * * * curl -4 -L http://127.0.0.1:5533/dns/update/www/
  */1 * * * * curl -6 -L http://[::1]:5533/dns/update/www/

  ```

- With crontab & log

  ```shell
  */1 * * * * curl -4 -L http://127.0.0.1:5533/dns/update/www/ >> /var/log/dns.log
  */1 * * * * curl -6 -L http://[::1]:5533/dns/update/www/ >> /var/log/dns.log

  # tail /var/log/dns.log -n 100
  # tail /var/log/dns.log -n 100 | grep <host>
  ```
