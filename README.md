<div align=center>
   <img src="https://github.com/zexvar/DDNSS/blob/main/logo.png" width=50% alt="DDNS Server">
</div>

# 项目介绍

DDNSS是一个开源的DDNS服务器(DDNS Server),
用于简化多台主机的DDNS服务,客户端无需进行额外安装,
通过http请求即可方便完成ip地址的更新(curl,wget...),
服务端在接收请求时直接获取请求的源ip.

- 项目采用Python语言+Flask框架开发,使用Docker方式部署.
- 服务器需要部署在支持ipv6的机器上!
- 仅支持对CloudFlare下托管的IPV6域名提供服务!

工作流程如下:

- 客户端向服务端发送请求
- 服务端获取客户端请求ip
- 服务端向CloudFlare更改域名记录的ip

| Client | ---> | DDNSS | ---> | Cloudflare |

## 项目部署

### A : Docker & Nginx (推荐)

1. 克隆此项目并进入DDNSS文件夹
    ```bash
    git clone https://github.com/zexvar/DDNSS
    cd DDNSS/
    ```

2. 打包成Docker镜像
    ```bash
    docker build -t ddns:latest .
    ```

3. 修改Nginx配置文件添加反向代理
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

### B : Docker (无需Nginx反代)

1. 克隆项目并打包成Docker镜像 (参考方法 A)
2. 启动容器,需要额外添加`--network=host`以支持Ipv6
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

使用MySQL数据库

   ```bash
   # SQLALCHEMY_ECHO: True
   SQLALCHEMY_TRACK_MODIFICATIONS: False
   SQLALCHEMY_DATABASE_URI: mysql+pymysql://root:123456@127.0.0.1:3306/ddns
   
   CLOUDFLARE:
     TOKEN: your cloudflare token
     ZONE_ID: your zone id
     ZONE_NAME: example.com
   ```

## 客户端使用

> 首次部署后需初始化数据库,在部署节点上执行: `curl http://127.0.0.1:5000/init/db`

> 请求首次携带key即为开启认证，之后所有请求都需要携带相同key

#### 基础使用

- `curl http://[::1]:5000/ddns/www`

以无认证方式更新www.example.com记录的ip

#### 开启身份验证

- `curl http://[::1]:5000/ddns/www1?key=123456`
- `curl http://[::1]:5000/ddns/www2?key=abc`

首次携带key请求自动设置key,之后请求需携带相同key(不同域名key可以不同)

#### 设置crontab定时任务

- `*/5 * * * * curl http://[::1]:5000/ddns/www > /root/ddns.log 2>&1`




