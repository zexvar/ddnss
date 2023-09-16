<div align=center>
   <img src="logo.png" width=50% alt="DDNS Server">
</div>

# 项目介绍

DDNSS 是一个开源的 DDNS 服务器(DDNS Server),用于简化多台主机的 DDNS 服务,客户端无需进行额外安装,通过 http 请求快速完成 ip 地址的更新,服务端在接收请求时直接获取请求的源 ip.

- 基于 Python 语言使用 Flask 框架开发.
- 通过 CloudFlare API 完成 ip 地址更新.
- 支持 IPV4/IPV6 协议(IPV6 需要机器支持).
- 支持 Docker 镜像方式快速部署.

## 服务端部署

打包为 Docker 镜像

```bash
# from github
docker build https://github.com/zexvar/ddnss.git -t ddnss:latest
# from source code
git clone https://github.com/zexvar/ddnss
cd ddnss && docker build -t ddnss:latest .
```

### A : Docker & Nginx (推荐)

启动容器

```shell
docker run -d --name=ddnss \
-v /opt/ddnss/:/ddnss/data \
-e TZ="Asia/Shanghai" \
-p 5000:5000 \
--restart=always \
ddnss:latest
```

添加 Nginx 反向代理

```nginx
server {
    listen      80;
    listen [::]:80;

    server_name  ddns.*;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:5000;
    }
}
```

### B : Docker only

添加`--network=host`以支持 Ipv6

```bash
docker run -d --name=ddnss \
-v /opt/ddnss/:/ddnss/data \
-e TZ="Asia/Shanghai" \
--restart=always \
--network=host \
ddnss:latest
```

## 客户端使用

### 基础使用

- `curl -4 http://127.0.0.1:5000/ddns/www`
- `curl -6 http://[::1]:5000/ddns/www`

以无认证方式更新www.example.com记录的ip

### 密钥认证

- `curl -4 http://127.0.0.1:5000/ddns/www?key=abc123`
- `curl -6 http://[::1]:5000/ddns/www?key=abc123`

首次携带 key 请求自动设置 key,之后请求需携带相同 key(不同域名 key 可以不同)

### 设置定时任务(crontab)

- `*/1 * * * * curl -4 http://127.0.0.1:5000/ddns/www`
- `*/1 * * * * curl -6 http://[::1]:5000/ddns/www`

保存所有更新日志

- `*/1 * * * * curl -4 http://127.0.0.1:5000/ddns/www >> /root/ddns.log`
- `*/1 * * * * curl -6 http://[::1]:5000/ddns/www >> /root/ddns.log`

最近日志 `tail /root/ddns.log -n 100`

查找日志 `tail /root/ddns.log -n 100 | grep <host>`
