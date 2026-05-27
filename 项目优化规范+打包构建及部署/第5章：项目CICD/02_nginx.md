# nginx
## 一：nginx工作原理
  > nginx  -->  一个master进程 --> 开启n个worker进程，一般设置为CPU核数  --> n个client(一个worker进程对应n个client连接)
  ### 1.概念:
  - master
  - worker
  ### 2.worker如何进行工作的？
  - worker进行争强式的方式来抢夺mster发布的任务
  ### 3.一个master和多个worker的好处:
    - （1）可以使用nginx -s reload 进行热部署，利用nginx进行热部署操作
    - （2）每个worker都是独立的进程，如果有其中饿一个worker出现问题，其他worker独立的继续进行争强，实现请求过程，不会造成服务中断
  ### 4.设置多少个worker合适?
    - worker数和服务器的cpu数相等是最为适合的，不会造成cpu资源闲置，也不会导致cpu过忙。
  **连接数worker_connection相关问题**
  ### 5.发送一个请求占用了worker几个连接数?
    - 静态资源2个，使用tomcat访问数据库时4个
  ### 6.nginx有一个master，有四个worker，每个worker支持最大的连接数据1024，支持的最大并发数是多少？
    - 普通的静态访问最大并发数是：worker_connections * worker_process / 2
    - 如果是作为反向代理来说，最大的并发数量应该是worker_connection * worker_process / 4
## 二：nginx代理
  > 正向代理和反向代理的作用和目的不同。**正向代理主要是用来解决访问限制问题**。而**反向代理则是提供负载均衡、安全防护等作用**。二者均能提高访问速度。
  ### 1.正向代理：**代理IP**代理了**客户端**，去和**目标服务器**进行交互。
  - **（1）突破访问限制**：通过代理服务器，可以突破自身IP访问限制，访问国外网站，教育网等。
  - **（2）提高访问速度**：通常代理服务器都设置一个较大的硬盘缓冲区，会将部分请求的响应保存到缓冲区中，当其他用户再访问相同的信息时， 则直接由缓冲区中取出信息，传给用户，以提高访问速度。
  - **（3）隐藏客户端真实IP**：上网者也可以通过这种方法隐藏自己的IP，免受攻击。
  ### 2.反向代理："代理服务器"代理了"目标服务器"，去和"客户端"进行交互。暴露的是代理服务器地址，隐藏了真实的服务器IP地址。
  - **（1）隐藏服务器真实IP**： 使用反向代理，可以对客户端隐藏服务器的IP地址。
  - **（2）负载均衡**：反向代理服务器可以做负载均衡，根据所有真实服务器的负载情况，将客户端请求分发到不同的真实服务器上。
  - **（3）提高访问速度**:反向代理服务器可以对于静态内容及短时间内有大量访问请求的动态内容提供缓存服务，提高访问速度。
  - **（4）提供安全保障**：反向代理服务器可以作为应用层防火墙，为网站提供对基于Web的攻击行为（例如DoS/DDoS）的防护，更容易排查恶意软件等。还可以为后端服务器统一提供加密和SSL加速（如SSL终端代理），提供HTTP访问认证等。
  - 例如：在访问www.123.com(该域名不存在，纯粹是window的host文件配置映射的虚拟地址)时我们通过nginx代理服务器(192.168.17.129:80)访问到tomcat服务（127.0.0.1:8080）
  - **proxy_set_header**:更改nginx服务器接收到的客户端请求的请求头信息，然后将新的请求头发送到代理的服务器
  - **proxy_redirect**:用来重置头信息中的location和refresh,default|off|redirect(目标) replacement(要替换的值)
    ```js
      // 代理服务器：192.168.2.133
      server {
        listen 8080
        location /server {
          proxy_pass http://192.168.10.1/
          proxy_set_header username TOM
        }
      }
      // 被代理服务器：192.168.10.1
      server {
        listen 8080
        server_name localhost;
        default_type test/plain;
        return 200 $http_username
      }
    ```
  ### 3.nginx添加SSL支持：
  - 将原有的/usr/local/nginx/sbin/nginx进行备份
  - copynginx之前的配置信息
  - nginx安装源码进行配置指定对应模块 ./configure --with-http_ssl_module
  - 通过make模版进行编译
  - 将objs下的nginx移动到usr/local/nginx/sbin下
  - 再源码目录下执行make upgrade进行升级，从而实现不停机添加新模块的功能
  ### 4.nginx反向代理调优：反向代理值Buffer和Cache
  - buffer缓冲用来解决不同设备之间数据传递速度不一致导致的性能低的问题，缓冲数据操作完成后就可以删除
  - cache缓存是备份，数据缓存到代理服务器一份，可以重复使用
## 三：nignx负载均衡
  > 负载均衡用来解决服务器超出并发能力，或者宕机等情况
  ### 应用集群：将同一个应用部署到多台机器上，组成处理集群，接收负载均衡设备分发的请求，进行处理并返回响应数据
  ### 负载均衡器：将用户访问的请求根据对应的负载均衡算法分发到集群中的某一台服务器进行处理
  ### 1.分配服务器策略：
  - (1)轮训策略：upsteam模块负载均衡的默认策略，每个请求按照时间顺序逐一分配到不同的后端服务器，如果某个服务器down掉能自动剔除
  - (2)权重策略：weight
  - (3)源地址哈希：ip_hash,定向分发，保持会话，每个请求按照访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，比如某个请求上次访问的是80下次继续访问该端口
  - (4)least_conn
  ### 2.四层均衡与七层均衡

  ### 3.配置关键字：
  - **weight**:weight代表权重，权重越高被分配的客户端越多
  - **down**:该服务器不参与负载均衡
  - **backup**：备用机，当所有机器都不能用时才会启用
  - **max_fails**：限制最大的连接失败数
  - **fail_timeout**：限制超时时间
  - **max_conns**：限制最大的接收连接数
  - **fair(第三方插件)**：按照服务器的响应时间分配，响应时间短的优先
  ```js
    http {
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
## 五：rewrite伪静态，rewrite伪静态配置，rewrite域名跳转
  ### 1.rewrite防盗链
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
  ### 2.指令：
  - $args：请求URL的请求参数
  - $host:访问服务器的server_name的值
  - $document_uri
  - $request_uri
  - $http_user_agent:用户访问读物的代理信息
  - return指令：用于完成对请求的处理，直接向客户端返回
  - rewrite指令：
  - rewrite_log指令：是否开启URL重写日志
  ```js
    server {
      location / {
        rewrite ^/2.html$   /index.jsp?pageNum=2 break;
      }
    }
    server {
      listen 80;
      server_name www.itheima.cn www.XXX.com;
      rewrite ^(.*) http:www.XXX.cn$1;
    }
  ```
  ### 3.域名镜像:平衡网站的流量负载
    ```js
      server {
        listen 80;
        server_name www.itheima.cn www.XXX.com;
        location /user {
          rwwrite ^^/user(.*)$ http:www.xxx.com;
        }
      }
    ```
  ### 4.独立域名：一个项目中的多个模块有自己独立的域名
    ```js
      server {
        listen 81;
        server_name search.XXX.com;
        rewrite ^(.*) http://www.xxx.cn/search$1;
      }
      server {
        listen 81;
        server_name search.XXX.com;
        rewrite ^(.*) http://www.xxx.cn/search$1;
      }
    ```
## 六：return网址跳转，http自动跳转到https
## 七：nginx多站点配置
  ### 1.方式一：多端口
  ```js
    server {
      8080;
      location / {
        /web/firstWeb
        index index.html index.htm;
      }
    }
    server {
      8081;
      location / {
        /web/secondWeb
        index index.html index.htm;
      }
    }
  ```
  ### 2.方式二：多ip
  ### 3.方式三：多域名

## 八：缓存
  ### 服务端缓存:nginx/redis
  - proxy_cache_path:缓存路径
  - pxoy_cache:开启或者关闭代理缓存
  - proxy_cache_key:nginx会根据key值MD5哈希来存缓存
  - proxy_cache_valid:对不同返回状态码的URL设置不同的缓存事件
  - proxy_cache_min_uses:设置资源被访问多少次后被缓存
  - proxy_cache_methods:设置哪些请求方式被缓存
  - levels:指定该缓存的目录
  - keys_zone:用来为这个缓存区设置名称和指定大小，keys_zone=itcast:200m
  ```js
  server {
    proxy_cache_path: /usr/local/proxy_cache
  }
  ```
  ### 客户端缓存：浏览器缓存
## 九：nginx日志
  ### 1.访问日志access.log
  ### 2.错误日志error.log记录nginx本身运行时的错误信息
  日志级别有：debug,info,notice,warn,error,crit,alert,emerg

## 十：nginx高可用配置
  > 发生前提当nginx服务挂机时服务就会中断，所以才会出现高可用模式。需要多台nginx服务器和keepalived脚本检测服务是否可用前提 

## 十一：nginx配置项
  ### 1.user:用来配置nginx服务器的worker进程的用户和用户组，默认nobody
  ### 2.work
  ps -ef | grep nginx查看开启了几个进程和线程
  ### 3.events块
  涉及nginx和用户之间的网络连接，比如worker_connection.常用的配置包括是否开启对多worker process下的网络连接进行序列化，是否允许同时接收多个网络连接，选取哪种事件驱动模型来处理连接请求，每个worker process可以同时支持的最大连接数等。
  - **accept_mutex**:用来设置nginx网络连接序列化
  - **multi_accpet**:用来设置是否允许同事接收多个网络连接
  - **work_connections**:用来配置单个worker进程最大的连接数
  - **use**:值有select/poll/epoll/kquue,用来设置nginx服务器选择哪种事件驱动来处理网络消息
  ### 4.http
  http全局块配置的指令包括文件引入，日志自定义，连接超时时间，MIME-TYPE定义，单链接请求数上限等。默认有两行配置include，default_type
  - **default_type**：位置可以在http,server,location中
  - **sendfile**:on|off
    - 设置nginx服务器是否使用sendfile传输文件，可以提高nginx处理静态资源的性能。
    - sendfile使用前：应用程序缓冲区 ---->  请求读取内核缓冲区的index.html资源 --> index.html资源先copy到内核缓冲区 ---> 内核缓冲区再将资源copy给应用程序缓冲区--->应用缓存区再copy给socket缓冲区 --> socket缓冲区发送给客户端
    - 使用sendfile后：应用程序缓冲区sendfile ---->  请求读取内核缓冲区的index.html资源 --> index.html资源先copy到内核缓冲区 --->内核缓冲区直接将数据发送给socket缓冲区 --> socket缓冲区发送给客户端
  - **tcp_nopush**:前提是sendfile开启，用来提升网络包的传输效率
  - **tcp_nodelay**:前提是keep-alive开启时才生效，提高网络包传输的实时性
  - **keepalive_timeout**:用来设置长连接的超时时间
  - **keepalive_requests**:用来设置一个keepalive连接使用的次数
  ### 5.server
  - server_name,匹配顺序，精准<通配符在前面<通配符在后面<正则<default_server
  ### 6.location
  - **try_files**：用于处理静态文件请求,$uri是请求的原始URI
  - **root**:定义了资源的根目录，server的服务根目录。
    - root path,path为nginx服务器接收到请求后查找资源的根目录，root的处理结果是：root路径+locatin路径
  - **alias**:用来更改location的URI。
    - alias path为修改后的根路径,alias的处理结果是：alias路径替换location路径。
    - 如果location路径是以/结尾，alias也必须以/结尾，root无要求
  ```js
    server {
      location /images {
        root  /usr/local/nginx/html // 处理结果：/usr/local/nginx/html/images/XXX.png
        index  index.html index.htm;
        try_files $uri $uri/ /index.html; // 解决vue项目history的路由刷新问题
        error_page  404              /404.html;
        error_page 404 =200 /idnex.html;//将404转成200返回index.html
        error_page   500 502 503 504  /50x.html;
      }
      location /images/ {
        alias /usr/local/nginx/html/images/ // 处理结果：/usr/local/nginx/html/images/xxx.png
      }
    }
  ```
  - **index**:设置网站的默认首页,可以是ip+port
  - **error_page**:设置网站的错误页面
  ### worker_processes：worker_process值越大，可以支持的并发处理量也越大，但是会收到硬件，软件等设备的制约
  ### include:用来引入其他配置文件，使nginx配置更加灵活


## nginx常用变量
  - $args:请求参数
  - $content_length:http响应信息里面的COntent-Length
  - $content_type:http响应信息里面的Content-type
  - $document_root:nginx虚拟主机配置文件中的root站点根目录
  - $document_url:当前请求中不包含指令的URI,
  - $host:主机头，域名或者ip地址
  - $http_user_agent:客户端的详细信息，浏览器标识
  - $http_cookie:客户端的cookie信息
  - $http_referer:客户端请求的referer键值对，可以用来防盗链
  - valid_referers:none：检测不存在Referer的情况/blocked/server_names单个或者多个URL,检测Referer头域的值是否是其中之一/strings

## nginx常用操作命令：
  ```js
    start nginx // 启动服务
    nginx -s stop // 停止服务
    nginx -s reload //nginx重启服务
    nginx -s restart
    nginx -t // 语法检查
  ```
## gzip压缩
  - gzip：on|off
  - gzip_types:压缩源文件类型
  - gzip_comp_level:gzip压缩级别
  - gzip_min_length:压缩的最小大小
  - gzip_buffers:用于处理请求压缩的缓冲区数据和大小
  - gzip_vary:响应头添加vary信息，告诉客户端使用了gzip压缩
  - gzip_disabled
  - gzip_proxied:nginx作为反向代理压缩服务端返回数据的条件

## nginx安装
  ### (1)ubuntu
  - apt-get update
  - apt install nginx
  - systemctl status nginx

  ### nginx的basic认证
  ### nginx的证书配置
  ### nginx的访问控制allow和deny
# nginx开启限流
  ### 漏桶算法
  ### 令牌算法
  ```js
    // 请求限流
    limit_req_zone $binary_remote_addr zone=conn_limit:10m;
    limit_conn conn_limit 1;// 限制连接数为1个
    limt_req zone=ip_limit burst=2 nodelay
  ```

## 附录
```js
    // user  nobody;
    worker_processes  1; // nginx服务器兵法处理服务的关键配置，worker_process值越大，可以支持的并发处理量也越大，但是会收到硬件，软件等设备的制约
    // error_log  logs/error.log;
    // error_log  logs/error.log  notice;
    // error_log  logs/error.log  info;
    // pid        logs/nginx.pid;
    events {
        worker_connections  1024; // 每个worker可以支持的最大连接数
    }
    http {
        include       mime.types;
        default_type  application/octet-stream; // 传递给客户端的数据类型

        // log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
        //                   '$status $body_bytes_sent "$http_referer" '
        //                   '"$http_user_agent" "$http_x_forwarded_for"';

        //access_log  logs/access.log  main;

        sendfile        on;// nginx应用内存发送信号sendfile给网络接口，网络接口直接读取服务器文件内容
        // tcp_nopush     on;

        // keepalive_timeout  0;
        keepalive_timeout  65;

        // gzip  on;

        server {
            listen       90; // nginx监听的端口号，一般该端口会被占用
            server_name  localhost; //

            // charset koi8-r;

            // access_log  logs/host.access.log  main;

            location / {
                root   home/www/dist;
                index  index.html index.htm;
                try_files $uri $uri/ /index.html;
                proxy_pass http://127.0.0.1:8080;
            }
            location /house/ {
                root   home/house;
                index  index.html index.htm;
                try_files $uri $uri/ /house/index.html;
                proxy_pass http://127.0.0.1:8080;
            }
            // error_page  404              /404.html;

            // redirect server error pages to the static page /50x.html
            #
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   html;
            }

            //  proxy the PHP scripts to Apache listening on 127.0.0.1:80
            // 
            // location ~ \.php$ {
            //     proxy_pass   http://127.0.0.1;
            // }

            //  pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
            // 
            // location ~ \.php$ {
            //     root           html;
            //     fastcgi_pass   127.0.0.1:9000;
            //     fastcgi_index  index.php;
            //     fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
            //     include        fastcgi_params;
            // }

            //  deny access to .htaccess files, if Apache's document root
            //  concurs with nginx's one
            // 
            // location ~ /\.ht {
            //     deny  all;
            // }
        }
        //  another virtual host using mix of IP-, name-, and port-based configuration
        // 
        // server {
        //     listen       8000;
        //     listen       somename:8080;
        //     server_name  somename  alias  another.alias;// 
        //     location / {
        //         root   html;
        //         index  index.html index.htm;
        //     }
        // }// 
        //  HTTPS server
        // 
        // server {
        //     listen       443 ssl;
        //     server_name  localhost;// 
        //     ssl_certificate      cert.pem;
        //     ssl_certificate_key  cert.key;

        //     ssl_session_cache    shared:SSL:1m;
        //     ssl_session_timeout  5m;// 
        //     ssl_ciphers  HIGH:!aNULL:!MD5;
        //     ssl_prefer_server_ciphers  on;// 
        //     location / {
        //         root   html;
        //         index  index.html index.htm;
        //     }
        // }
    }
  ```
## 配置实例
/home/www
|__conf.d
|__mweb
  |__404.html
  |__server1
  |  |__location1
  |  |  |__index_src1_location2.html
  |  |__location2
  |  |  |__index_src1_location2.html
  |  |__log
  |__server2
  |  |__location1
  |  |  |__index_src1_location2.html
  |  |__location2
  |  |  |__index_src1_location2.html
  |  |__log
```js
  
```