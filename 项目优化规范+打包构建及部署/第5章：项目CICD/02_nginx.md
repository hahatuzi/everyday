# nginx
## 一：nginx工作原理
  nginx  -->  一个master进程 --> 开启n个worker进程  --> n个client(一个worker进程对应n个client连接)
  worker如何进行工作的？
  worker进行争强式的方式来抢夺mster发布的任务
    **1.一个master和多个worker的好处**
    答：（1）可以使用nginx -s reload 进行热部署，利用nginx进行热部署操作
        （2）每个worker都是独立的进程，如果有其中饿一个worker出现问题，其他worker独立的继续进行争强，实现请求过程，不会造成服务中断
  **2.设置多少个worker合适**
    答：worker数和服务器的cpu数相等是最为适合的，不会造成cpu资源闲置，也不会导致cpu过忙。
  **连接数worker_connection相关问题**
  **3.发送一个请求占用了worker几个连接数：**
    答：静态资源2个，使用tomcat访问数据库时4个
  **4.nginx有一个master，有四个worker，每个worker支持最大的连接数据1024，支持的最大并发数是多少？**
    答：普通的静态访问最大并发数是：worker_connections * worker_process / 2
    如果是作为反向代理来说，最大的并发数量应该是worker_connection * worker_process / 4
    每个worker最大支持的连接数
## 二：nginx代理
  > 正向代理和反向代理的作用和目的不同。**正向代理主要是用来解决访问限制问题**。而**反向代理则是提供负载均衡、安全防护等作用**。二者均能提高访问速度。
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
  - 例如：在访问www.123.com(该域名不存在，纯粹是window的host文件配置映射的虚拟地址)时我们通过nginx代理服务器(192.168.17.129:80)访问到tomcat服务（127.0.0.1:8080）

## 三：nignx负载均衡，分配服务器的策略如下：
  ### 1.分配服务器策略
  - (1)轮训策略：每个请求按照时间顺序逐一分配到不同的后端服务器，如果某个服务器down掉能自动剔除
  - (2)权重策略：
  - (3)源地址哈希：ip_hash,定向分发，保持会话，每个请求按照访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，比如某个请求上次访问的是80下次继续访问该端口
  ### 2.配置关键字：
  - weight:weight代表权重，权重越高被分配的客户端越多
  - down:该服务器不参与负载均衡
  - backup：备用机，当所有机器都不能用时才会启用
  - fair(第三方插件)：按照服务器的响应时间分配，响应时间短的优先
  ```js
    http {-
      upstream myserver {
        ip_hash;
        server 115.28.52.63:8080 weight=1;
        server 115.28.52.63:8081 weight=1;
        server 115.28.52.63:8082 weight=1 down; // down不参与负载均衡
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

## 四：动静分离
  > 为了加快网站的解析速度，可以把动态页面和静态页面由不同的服务器来解析，加快解析速度，降低单个服务器的压力

## 五：伪静态
## 六：防盗链
  > $http_referer:客户端请求的referer键值对，可以用来防盗链
   ```js
    // html文件中添加<meta name="referer" content="no-referer">可以用来反防盗链
    location ~* .*\.(gif|png|jpg)$ {
      if ( $http_referer !~* *a.baidu.com*) { // !~*为不包含的意思，代表访问图片网址只要不是a.baidu.com都不允许访问图片资源
        return 403
      }
      // valid_referers
      valid_referers none 192.168.44.1
      if($valid_referers){
        // return 403;
        rewrite ^/ /img/error.png break; // 返回盗链报错处理图片
      }
    }
  ```

## 七：nginx日志
  ### 1.访问日志
  ### 2.错误日志

## 八：nginx高可用配置
  > 发生前提当nginx服务挂机时服务就会中断，所以才会出现高可用模式。需要多台nginx服务器和keepalived脚本检测服务是否可用前提 

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
  ### worker_processes：
  ### worker_connections：每个worker可以支持的最大连接数
## nginx安装
  ### (1)ubuntu
  - apt-get update
  - apt install nginx
  - systemctl status nginx