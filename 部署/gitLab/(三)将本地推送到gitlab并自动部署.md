# 静态服务器apache,或者nginx安装
#### 第一步：检查是否有旧版本的apache
rpm -qa | grep httpd 
#### 第二步：安装
yum -y install httpd
#### 第三步：再次检查是否安装成功
rpm -qa | grep httpd
#### 第四步：启动apache,并修改端口号,因为gitlab服务可能占用了apache的默认端口80.
service httpd start
```js
[root@iZq0jkhg8vdxw3Z gitlab]# cd /var/www/html/
[root@iZq0jkhg8vdxw3Z html]# ls
[root@iZq0jkhg8vdxw3Z html]# cd /etc/httpd
[root@iZq0jkhg8vdxw3Z httpd]# ls
conf  conf.d  conf.modules.d  logs  modules  run
[root@iZq0jkhg8vdxw3Z httpd]# cd conf
[root@iZq0jkhg8vdxw3Z conf]# ls
httpd.conf  magic
[root@iZq0jkhg8vdxw3Z conf]# vi httpd.conf
```
#### 第五步：部署资源
每次pipeline的时候将本地机器代码远程拷贝到云服务器上
sshpass -p $password scp -r ./build $custom_username@custom_ip:var/www/html
(1)需要在gitlab-ci.yml文件中添加
  script: 
    - sshpass -p 812a1998D scp ./index.html root@47.99.144.3:/var/www/html
（2）在远程服务器上添加sshpass:
  yum -y install sshpass
(3)关闭部署时报错Host key verification failed.
vim /etc/ssh/ssh_config
修改ssh——config文件中的 StrictHostKeyChecking为no
#### 第六步：创建远程域文件夹(可选)
默认情况下，文件存储在主机上的 “/var/www/html”中。
/var/www
├── cgi-bin
├── html

此路径也称为“DocumentRoot”（文档根目录），它用作服务器上网站的默认入口点。
为了存储多个网站，您需要在“/var/www/”中创建多个文件夹，并修改httpd配置文件以指向这些目录。
在本例中，让我们创建以下目录结构。
/var/www
├── cgi-bin
├── html
└── linuxmi.com
    ├── html
    └── log

为您的新网站创建专用文件夹。
**[root@localhost html]# mkdir -p /var/www/linuxmi.com/html**

确保创建文件以存储网站的日志文件。
**[root@localhost html]# mkdir -p /var/www/linuxmi.com/log**
现在您的文件夹已准备就绪，您可以创建要显示给用户的第一个HTML页面。

创建一个名为“ index.html”的新HTML文件，并将以下内容粘贴到其中。
**cd /var/www/linuxmi.com/html sudo vi index.html**

#### 注
Apache的默认配置文件路径：
（1）网站的根目录指向/var/www/html目录
(2)主配置文件时/etc/httpd/conf/httpd.conf
(3)存储在/etc/httpd/conf.d/目录
#### 七：阿里云服务器部署node环境，因为yml脚本运行时用到了npm命令
1. 执行以下命令，下载Node.js的安装包。
```js
wget https://npm.taobao.org/mirrors/node/v12.4.0/node-v12.4.0-linux-x64.tar.xz
```
2. 执行以下命令，解压Node.js的安装包。
```js
tar -xvf node-v12.4.0-linux-x64.tar.xz
```
3. 执行以下命令，重命名Node.js安装目录。
```js
mv node-v12.4.0-linux-x64/ /usr/local/node
```

其次：配置Node.js

1. 执行以下命令，将Node.js的可执行文件目录加入到系统环境变量中。
```js
echo "export PATH=$PATH:/usr/local/node/bin" >> /etc/profile
```
2. 执行以下命令，使刚配置的Node.js环境变量立即生效。
```js
source /etc/profile
```
3. 执行以下命令，分别查看node和npm版本。
```js
node -v
npm -v
```

然后：测试Node.js环境

1.使用vim命令创建一个测试文件。
```js
vim HelloWorld.js
```
2. 输入i进入编辑模式。

复制如下代码到HelloWorld.js文件中。
```js
var http = require('http');
http.createServer(function (request, response) {
response.writeHead(
200,
{
'Content-Type': 'text/plain'
});
response.end('Hello World\n');
}).listen(8080);
console.log('Server started');
```
按Esc键退出编辑模式，输入侧:wq保存退出。

3.执行以下命令，运行HelloWorld.js文件。
node HelloWorld.js
4 打开浏览器，在地址范围输入http://<ECS公网地址>:8080，例如http://127.0.0.0:8080。

如果返回如下界面，则表示成功。

[!使用Docker Compose、Nginx、SSH和Github Actions实现前端自动化部署测试机]https://blog.csdn.net/qq_34998786/article/details/122227957?spm=1001.2014.3001.5502