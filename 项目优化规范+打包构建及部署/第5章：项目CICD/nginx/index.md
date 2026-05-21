# 1.启动服务start nginx
# 2.修改默认访问端口80
# 3.停止服务 nginx -s stop
# 4.nginx重启服务 nginx -s reload
# nginx -t语法检查
# 5.新建网站文件夹
# 6.nginx配置文件学习
(1)location
try_files $url $url /index.html
// 解决vue项目history的路由刷新问题
[!参考文章]https://cloud.tencent.com/developer/article/1647191



## nginx多站点配置
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

# nginx的basic认证
# nginx的证书配置
# http自动跳转到https
## return网址跳转
## rewrite伪静态配置，网址跳转
  ```js
    server {
      location / {
        rewrite ^/2.html$   /index.jsp?pageNum=2 break;
      }
    }
  ```
# nginx的访问控制allow和deny
## gzip压缩
# nginx开启限流
  ### 漏桶算法
  ### 令牌算法
  ```js
    // 请求限流
    limit_req_zone $binary_remote_addr zone=conn_limit:10m;
    limit_conn conn_limit 1;// 限制连接数为1个
    limt_req zone=ip_limit burst=2 nodelay
  ```
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