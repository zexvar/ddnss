<div align=center>
   <img src="https://github.com/zexvar/DDNSS/blob/main/logo.png" width=50% alt="DDNS Server">
</div>

# 项目介绍

DDNSS 是一个开源的 DDNS 服务器(DDNS Server),
用于简化多台主机的 DDNS 服务,客户端无需进行额外安装,
通过 http 请求即可方便完成 ip 地址的更新(curl,wget...),
服务端在接收请求时直接获取请求的源 ip.

- 此项目基于 Python 语言使用 Flask 框架开发.
- 仅支持对 CloudFlare 下托管的域名提供服务.
- 支持 IPV4/IPV6 协议(IPV6 需要部署机器支持).
- 此项目支持通过 Docker 方式进行快速部署.

工作流程如下:

- 客户端向服务端发送更新域名记录请求
- 服务端解析客户端请求 IP 和对应域名记录 ID
- 服务端向 CloudFlare 更改域名记录内容

```mermaid
sequenceDiagram
    participant Client
    participant DDNSS
    participant Cloudflare
    Client->>+DDNSS: Update record request
    DDNSS->>+Cloudflare: Cloudflare API
    Cloudflare->>-DDNSS: Operation result
    DDNSS->>-Client: Current record content
```

## 项目部署

### A : Docker & Nginx (推荐)

1. 克隆此项目并进入 DDNSS 文件夹

   ```bash
   git clone https://github.com/zexvar/DDNSS
   cd DDNSS/
   ```

2. 打包成 Docker 镜像

   ```bash
   docker build -t ddns:latest .
   ```

3. 修改 Nginx 配置文件添加反向代理
   ```bash
   server {
      listen [::]:80;
      listen [::]:443 ssl;
      server_name  ddns.example.com;
      location / {
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_pass http://127.0.0.1:5000;
      }
   }
   ```

4. 启动容器
   ```shell
   # config.yml 需提前创建
   docker run -d --name=ddns \
   -v /opt/ddns/config.yml:/opt/ddns/config.yml \
   -e TZ="Asia/Shanghai" \
   -p 5000:5000 \
   --restart=always \
   ddns:latest
   ```

### B : Docker only

1. 克隆项目并打包成 Docker 镜像 (参考方法 A)
2. 启动容器,需要额外添加`--network=host`以支持 Ipv6
   ```bash
   # config.yml 需提前创建
   docker run -d --name=ddns \
   -v /opt/ddns/config.yml:/opt/ddns/config.yml \
   -e TZ="Asia/Shanghai" \
   --restart=always \
   --network=host \
   ddns:latest
   ```

## 配置文件

使用 MySQL 数据库

```bash
SQLALCHEMY_TRACK_MODIFICATIONS: False
SQLALCHEMY_DATABASE_URI: mysql+pymysql://root:123456@127.0.0.1:3306/ddns

CLOUDFLARE:
  TOKEN: your cloudflare token
  ZONE_ID: your zone id
  ZONE_NAME: example.com

# Optional
# DDNS_KEY: abc123
```

## 客户端使用

> 首次部署后需初始化数据库,在部署节点上执行: `curl http://127.0.0.1:5000/init/db`

> 配置文件中设置 DDNS_KEY 开启权限认证

#### 基础使用

- `curl http://ip:5000/ddns/www`

以无认证方式更新www.example.com记录的ip

#### 开启身份验证

- `curl http://ip:5000/ddns/www?key=abc123`

首次携带 key 请求自动设置 key,之后请求需携带相同 key(不同域名 key 可以不同)

#### 设置 crontab 定时任务

- `*/5 * * * * curl http://ip:5000/ddns/www -o /root/ddns/www.log`
