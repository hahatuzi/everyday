# 1.启动服务start nginx
# 2.修改默认访问端口80
# 3.停止服务 nginx -s stop
# 4.nginx重启服务 nginx -s reload
# 5.新建网站文件夹
# 6.nginx配置文件学习
(1)location
try_files $url $url /index.html
// 解决vue项目history的路由刷新问题
[!参考文章]https://cloud.tencent.com/developer/article/1647191