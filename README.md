# DDNSS
## DDNS Server
### 项目介绍

- 此项目仅支持 Ipv6 DDNS
- 此项目仅支持 Cloudflare 管理的域名
- 此项目为了简化多主机进行 DDNS 的操作配置

### 基本流程

Client -> DDNSS -> Cloudflare

### 项目服务端部署

> 通过源码部署

1. git clone 或 下载代码
2. 安装依赖 `pip install -r requirement.txt`
3. 运行程序
    ```shell
    # 修改配置文件
    vim config.yml
    chmod +x init.sh && ./init.sh
    ```
4. 初始化数据库 `curl http://127.0.0.1:5000/init`

> 通过Docker部署

1. git clone 或 下载代码
2. 打包为docker镜像 `docker build -t ddns:latest .`
3. 运行容器 ( 添加`--network=host` 以支持ipv6 )
    ```shell
   # config.yml 需提前创建
   docker run -d --name=ddns \
   -v /opt/ddns/config.yml:/opt/ddns/config.yml \
   --restart=always \
   --network=host \
   ddns:latest
    ```
4. 需要设置 --network=host 使用主机网络

> 通过Docker & Nginx部署

1. git clone 或 下载代码
2. 打包为docker镜像 `docker build -t ddns:latest .`
3. 运行容器 (无须添加`--network=host`)
    ```shell
   # config.yml 需提前创建
   docker run -d --name=ddns \
   -v /opt/ddns/config.yml:/opt/ddns/config.yml \
   -p 5000:5000 \
   --restart=always \
   ddns:latest
    ```
4. 修改nginx配置文件
   ```shell
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

### 客户端进行DDNS服务

> 请求首次携带key即为开启认证，之后所有请求都需要携带相同key

- 不进行身份验证 curl http://127.0.0.1:5000/ddns/www
- 开启身份验证 curl http://127.0.0.1:5000/ddns/www?key=123456
- 利用crontab设置 `*/5 * * * * curl http://ddns.example.com:5000/ddns/* > /ddns.log 2>&1`