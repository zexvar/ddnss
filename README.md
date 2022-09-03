# DDNS Cloudflare

### 项目简介
- 此项目仅支持ipv6 DDNS
- 此项目仅支持Cloudflare管理的域名
- 此项目用于作为DDNS服务端

### 基本流程
Server -> This project -> Cloudflare API

### 项目部署
- git clone 或 下载代码
- ```shell
  pip install -r requirements.txt
  # 修改配置文件
  vim app/config/config.yaml
  # gunicorn -b [::]:port run:app
  ./run.sh
  # 初始化数据库
  curl http://[your server ip]:port/init
  ```
  
### 进行DDNS服务
- 不进行mac地址验证 curl http://[your server ip]:port/ddns/www
- 开启mac地址验证 curl http://[your server ip]:port/ddns/www?mac=your mac address
