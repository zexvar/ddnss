<div align=center>
   <img src="logo.png" width=50% alt="DDNS Server">
</div>

# Overview

DDNSS is an open-source DNS server designed to simplify DNS services for managing multiple hosts. Clients can update IP addresses quickly and efficiently through HTTP requests without the need for additional server installations. The server automatically retrieves the source IP address from incoming requests.

### Features

- **Protocol Support**: Fully supports both IPv4 and IPv6 protocols.
- **Rapid Deployment**: Offers ready-to-use Docker images for quick and seamless deployment.
- **Cloudflare Integration**: Enables IP address updates through the Cloudflare API for enhanced functionality and reliability.

### Benefits

- Simplifies DNS management for dynamic IP environments.
- Easy to integrate and deploy in existing infrastructure.
- Open-source and actively maintained for continuous improvements.

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
  curl -4 -L http://server:5533/api/update?hostname=www
  curl -6 -L http://server:5533/api/update?hostname=www
  ```
- Wtih ip

  ```shell
  curl -4 -L http://server:5533/api/update?hostname=www&ip=127.0.0.1
  curl -6 -L http://server:5533/api/update?hostname=www&ip=::1
  ```

- Wtih auth

  ```shell
  curl -4 -L http://server:5533/api/update?hostname=www&token=123456
  curl -6 -L http://server:5533/api/update?hostname=www&token=123456
  ```

- With crontab

  ```shell
  */1 * * * * curl -4 -L http://server/api/update?hostname=www
  */1 * * * * curl -6 -L http://server:5533/api/update?hostname=www

  ```

- With crontab & log

  ```shell
  */1 * * * * curl -4 -L http://server:5533/api/update?hostname=www >> /var/log/dns.log
  */1 * * * * curl -6 -L http://server:5533/api/update?hostname=www >> /var/log/dns.log

  # tail /var/log/dns.log -n 100
  # tail /var/log/dns.log -n 100 | grep <host>
  ```
