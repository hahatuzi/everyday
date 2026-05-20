# nginx
## 一：代理
  ### 1.正向代理：**代理服务器**代理了**客户端**，去和**目标服务器**进行交互。
  - **（1）突破访问限制**：通过代理服务器，可以突破自身IP访问限制，访问国外网站，教育网等。
  - **（2）提高访问速度**：通常代理服务器都设置一个较大的硬盘缓冲区，会将部分请求的响应保存到缓冲区中，当其他用户再访问相同的信息时， 则直接由缓冲区中取出信息，传给用户，以提高访问速度。
  - **（3）隐藏客户端真实IP**：上网者也可以通过这种方法隐藏自己的IP，免受攻击。
    ```js
      server {
        resolver 192.168.1.109
        listen 80
        location / {
          proxy_pass 想要访问的url地址
        }.
      }
    ```
  ### 2.反向代理："代理服务器"代理了"目标服务器"，去和"客户端"进行交互。暴露的是代理服务器地址，隐藏了真实的服务器IP地址。
  - **（1）隐藏服务器真实IP**： 使用反向代理，可以对客户端隐藏服务器的IP地址。
  - **（2）负载均衡**：反向代理服务器可以做负载均衡，根据所有真实服务器的负载情况，将客户端请求分发到不同的真实服务器上。
  - **（3）提高访问速度**:反向代理服务器可以对于静态内容及短时间内有大量访问请求的动态内容提供缓存服务，提高访问速度。
  - **（4）提供安全保障**：反向代理服务器可以作为应用层防火墙，为网站提供对基于Web的攻击行为（例如DoS/DDoS）的防护，更容易排查恶意软件等。还可以为后端服务器统一提供加密和SSL加速（如SSL终端代理），提供HTTP访问认证等。

## 二：nignx负载均衡，分配服务器的策略如下：
  ### 1.轮训策略：每个请求按照时间顺序逐一分配到不同的后端服务器，如果某个服务器down掉能自动剔除
  ### 2.权重策略：weight代表权重，权重越高被分配的客户端越多
  ### 3.源地址哈希：ip_hash,定向分发，保持会话，每个请求按照访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，比如某个请求上次访问的是80下次继续访问该端口
  - fair(第三方)：按照服务器的响应时间分配，响应时间短的优先
  ```js
    http {
      upstream myserver {
        ip_hash;
        server 115.28.52.63:8080 weight=1;
        server 115.28.52.63:8081 weight=1;
        fair;
      }
      upstream web_cluster {
        server 192.168.10.1 weight=7 max_fails=3 fail_timeout=15; // 服务器A
        server 192.168.10.2 weight=3 max_fails=3 fail_timeout=15;// 服务器B，配置15秒内3次连接失败，就暂停分配流量
        server 192.168.10.3 backup;// // 服务器C,当A和B全部都不能用时才会启用
      }
      server {
        proxy_pass http://myserver;
        proxy_connect_timeout 10;
      }
    }
  ```


## 三：nginx日志
  ### 1.访问日志
  ### 2.错误日志
  

## nginx配置项
  ### (1)root:定义了资源的根目录，server的服务根目录
  ```js
    server {
      location /static/ {
        root  /var/www/html
      } 
      location / {
        root /html/zhenlin
        alias /html/zhelin/
      }
    }
    // 用户访问/static/images/logo.png  --->  root地址 + location + 访问地址--->  /var/www/html/static/images/logo.png
  ```
## nginx安装
  ### (1)ubuntu
  - apt-get update
  - apt install nginx
  - systemctl status nginx