CentOS7系统GitLab官方安装教程： https://about.gitlab.com/install/#centos-7
## 1、安装git依赖
yum install -y curl policycoreutils-python openssh-server
## 2.启动sshd服务
```js
// 设置开机自启动sshd服务
systemctl enable sshd
// 启动sshd服务
systemctl start sshd
```
## 3.配置防火墙（选填）
```js
// 第一步：开启防火墙
// 设置为开机自启动
systemctl enable firewalld
// 开启防火墙
systemctl start firewalld
// 第二步：添加http和https服务到firewalld，允许http/https服务通过, pemmanent表示永久生效，若不加--permanent系统下次启动后就会失效
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
// 第三步：重启防火墙
systemctl reload firewalld
// 对外开放端口
// 开放防火墙端口（以8080端口为例）
firewall-cmd --zone=public --add-port=8080/tcp --permanent
// 删除防火墙端口
firewall-cmd --zone=public --remove-port=8080/tcp --permanent
```
## 4.postfix配置(选填),postfix用来发送邮件
```js
// 第一步：安装postfix
yum install -y postfix
// 第二步：启动postfix
// 设置开机自启动
systemctl enable postfix
// 启动postfix
systemctl start postfix
// 查看是否启动成功（选填）
systemctl status postfix
```
## 5.安装gitlab
```js
// 下载gitlab镜像
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
// 安装gitlab
rpm -ivh gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
```
## 6.修改gitlab配置文件
```js
// 第一步：打开文件
cd /etc/gitlab
vi gitlab.rb
// 第二步：修改external_url和listen_url
```
## 6.重启
```js
gitlab-ctl reconfigure
gitlab-ctl restart
```
## 打开页面
**gitlab初次安装后，登录gitlab网页需要账号和密码**
账号为root，密码需要打开文件查看：vi /etc/gitlab/initial_root_password