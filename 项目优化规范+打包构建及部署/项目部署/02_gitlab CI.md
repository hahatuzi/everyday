# 一：gitlab CICD
  ### 1.组成
  - gitlab CI/CD
  - gitlab runner:是一个单独处理构建的应用程序，它可以单独部署，并通过API与gitlab CI/CD一起使用。**gitlab-runner可以在不同的主机上部署，也可以在同一个主机上设置多个gitlab-runner ,还可以根据不同的环境设置不同的环境，比如我们需要区分研发环境，测试环境以及正式环境等。**
  - gitlab-ci.yaml
  ### 2.工作流程
  push code --> trigger a pipeline --> gitlab-ci.yml --> gitlab CI pipelineCI pipeline(preparation -- build -- tests) --> Deploy对应多个gitlab runner(gitlab runner 可以是服务器或者docker容器)
  - 1.代码托管到git仓库
  - 2.项目根目录创建ci文件,gitlab-ci.yml,在文件中指定构建，测试和部署脚本
  - 3.gitlab检测到gitlab-ci.yml并使用gitlab runner 的工具运行脚本
  - 4.根据预定义的gitlab-ci.yml脚本分组成作业，并共同组成管道
  ### 3.gitlab CI/CD的特点
  - 1.多平台
  - 2.多语言
  - 3.稳定构建：构建与gitlab在不同的机器上运行
  - 4.并行构建：gitlab CI/CD在多态机器上拆分构建，从而实现快速执行
  - 5.实时日志记录
  - 6.灵活的管道
  - 7.版本管道：一个gitlab-ci.yml文件包含测试，整个过程的步骤
  ### 4.gitlab CI的完整流程
  - 第一步：阿里云服务器安装gitlab
  - 第二步：阿里云服务器安装gitlab-runner
  - 第三步：将本地推送到gitlab并自动部署
  ### 5.前端pipeline中需要的操作
  - 第一步：install阶段：就是执行npm install 命令，根据package.json安装node_modules依赖包
  - 第二步：eslint阶段: 执行eslint检查，判断代码格式是否符合规范，如果不符合停止pipeline
  - 第三步：build阶段: 编译成生产代码，可以通过webpack之类的打包工具执行编译，也可以通过脚手架自身提供的编译命令进行编译,如npm run build
  - 第四步：deploy阶段：部署阶段，将刚才的build阶端生成的生产代码部署到生产访问的服务器上，

# 二：gitlab安装及使用
  ### 1.安装方式一：使用rpm包安装
    ```js
      // CentOS7系统GitLab官方安装教程： https://about.gitlab.com/install/#centos-7
      // 第一步：下载gitlab镜像,低版本centos7用清华园镜像，centos8用packages.gitlab.com
      yum install curl policycoreutils-python openssh-server postfix wget -y
      // centos7
      wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
      // centos8
      wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ol/8/gitlab-ce-18.9.1-ce.0.el8.x86_64.rpm/download.rpm
      // 第二步：安装gitlab
      rpm -ivh gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
      // 第三步：编辑站点地址，修改external_url和listen_port
      vim /etc/gitlab.rb
      // 第四步：配置
      gitlab-ctl reconfigure
      // 第五步：重启
      gitlab-ctl restart
    ```
  ### 2.安装方式二：使用docker安装
    ```js
      mkdir -p ~/data/gitlub/config ~/data/gitlab/logs ~/data/gitlab/data
      docker pull gitlab/gitlab-ce:12.9.0-ce.0
    ```
  ### 3.gitlab常见命令
    ```js
      // 运行
      gitlab-runner run
      // 启动
      gitlab-runner start
      // 重启
      gitlab-runner restart
      // 通过name 取消注册
      gitlab-runner unregister --name develop
      // 删除所有注册runner
      gitlab-runner unregister --all-runners
    ```
  ### 4.gitlab安装的前置条件，可不做！！
  - （1）启动sshd服务
    ```js
      // 设置开机自启动sshd服务
      systemctl enable sshd
      // 启动sshd服务
      systemctl start sshd
    ```
  - （2）配置防火墙（选填）
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
  - （3）postfix配置(选填),postfix用来发送邮件
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

# 三：gitlab runner的安装与使用
  支持运行在目前常用的平台上，例如：Linux/Unix、Windows、MacOS、Docker容器内、Kubernetes。
  ### 1.概念
   - (1)gitlab Runner是一个开源项目，用于运行作业并将结果发送回gitlab。
   - (2)与gitlab CI结合使用，容器部署需要使用docker，gitlab runner版本应该和gitlab版本同步。
   - (3)可以根据需要配置任意数量的runner
   - (4)gitlab runner类似于jenkins的agent,执行CI持续集成，持续构建的脚本任务。
  ### 2.特点
  - (1)作业运行控制：同时执行多个作业
  - (2)作业运行环境：在本地使用docker容器，使用docker容器并通过SSH执行作业。
  - (3)允许自定义作业运行环境
  - (4)支持运行在目前常用的平台上，例如：Linux/Unix、Windows、MacOS、Docker容器内、Kubernetes。
  ### 3.Gitlab Runner的类型
    - (1)**shared:共享类型**，运行整个平台项目的作业(gitlab)
    - (2)**group:项目组类型**，运行特定group下所有项目的作业(group)
    - (3)**specific：项目类型**，运行指定的项目作业（project）
  ### 4.gitlab Runner的状态
    - (1)locked：锁定状态，无法运行项目作业。
    - (2)paused:暂停状态，不会运行作业。
  ### 5.gitlab Runner的安装
    -  (1)安装方式一：
      ```js
        // 第一步：添加gitlab官方库===============
        // For Debian/Ubuntu/Mint
        curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
        // For RHEL/CentOS/Fedora
        curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
        // 第二步：命令安装===============
        // MacOS
        sudo brew install gitlab-ci-multi-runner
        // For Debian/Ubuntu/Mint
        sudo apt-get install gitlab-ci-multi-runner
        //For RHEL/CentOS/Fedora
        sudo yum install gitlab-ci-multi-runner
      ```
    - (2)安装方式二：手动下载rpm包
      ```js
        // 无效命令：wget --content-disposition https://packages.gitlab.com/runner/gitlab-runner/packages/sles/12.5/gitlab-runner-18.9.0-1.x86_64.rpm/download.rpm
        // centos系统
        // 第一步：在https://gitlab-runner-downloads.s3.amazonawa.com/latest/index.html上站到最新的文件名和版本
        // 第二步：选择一个版本并下载二进制文件
        curl -LJO https://gitlab-runner-downloads.s3.amazonaws.com/latest/rpm/gitlab-runner-helper-images.rpm
        curl -LJO https://gitlab-runner-downloads.s3.amazonaws.com/latest/rpm/gitlab-runner_<arch>.rpm
        // 比如curl -LJO https://gitlab-runner-downloads.s3.amazonaws.com/latest/rpm/gitlab-runner_x86_64.rpm
        // 第三步
        rpm -i gitlab-runner_<arch>.rpm
        // 第四步
        rpm -Uvh gitlab-runner_<arch>.rpm
      ```
    - (3)安装方式三：通过docker安装
      ```js
        // 第一步：创建目录/data/devops/gitlab
        // 第二步：在devops文件夹下创建gitlab-runner文件夹
        // 第三步：gitlab文件夹下创建config文件夹
        // 第四步：cd至根目录
        // 第五步：
        docker run -itd -v /data/devops/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:v18.9.0
      ```
  ### 6.检查安装并使用
    ```js
      systemctl start gitlab-runner
      systemctl status gitlab-runner
      gitlab-runner -h
      // 运行
      gitlab-runner run
      // 启动
      gitlab-runner start
      // 重启
      gitlab-runner restart
      // 通过name 取消注册
      gitlab-runner unregister --name develop
      // 删除所有注册runner
      gitlab-runner unregister --all-runners
    ```
  ### 7.gitlab-runner注册:获取gitlab runner的token,然后进行注册
    - 方式一：交互式注册:gitlab-runner register
      ```js
        // 第一步：
        gitlab-runner register
        // ============gitlab-runner register的注册流程配置如下============
        Enter the GitLab instance URL (for example, https://gitlab.com/):
        http://47.99.144.3/
        Enter the registration token:
        meAG8N_apx3bsBCCxRpL
        Enter a description for the runner:
        [iZq0jkhg8vdxw3Z]: my-app
        Enter tags for the runner (comma-separated):
        my-app
        Enter optional maintenance note for the runner:

        Registering runner... succeeded                     runner=meAG8N_a
        Enter an executor: shell, virtualbox, docker-ssh+machine, instance, custom, docker, docker-ssh, parallels, kubernetes, ssh, docker+machine:
      ```
    - 方式二：非交互式注册
      ```js
        docker ps
        docker ps | grep gitlab
        docker exec -it xxxhash
        docker run -itd --rm -v ~/data/gitlab-ruunner/config/etc/gitlab-runner gitlab/gitlab-runner:v12.6.0 register \
        --non-interative \
        --executor 'shell' \
        --url "http://106.14.38.228/" \
        --registration-token "dwe1kTT9v8bZcqyBupB7" \
        --description "devops-runner" \
        --tag-list "build,deploy" \
        --run-untagged="true" \
        --locked="false" \
        --access-level="not_protected" 
         // locked-锁定
         // access-level-访问级别
      ```


# 四：执行器：Shell, Docker, Kubernetes

# 五：模板库
  ### 1.流程：目的：满足前后端各种场景下的打包需求，定义一个模板流水线工程
  - 第一步：创建一个git仓库用于存放模板
  - 第二步：在仓库内创建一个template目录用于存放所有pipeline的模板
  - 第三步：在仓库内创建一个jobs目录存放job模板
  ### 2.前端npm集成
  - 第一步：install阶段：执行npm install 命令，根据package.json安装node_modules依赖包
  - 第二步：eslint阶段：执行eslint检查，判断代码格式是否符合规范，如果不符合停止pipeline
  - 第三步：build阶段：编译成生产代码，可以通过webpack之类的打包工具执行编译，也可以通过脚手架自身提供的编译命令进行编译,如npm run build
  - 第四步：deploy阶段：部署阶段，将刚才的build阶端生成的生产代码部署到生产访问的服务器上，
  ```js
  ```

# 六：
  ### 1.SonarQube代码扫描
    - 第1步：在centos8上下载sonar-scanner客户端
  ### 2.git pull请求集成配置

# 七.ssl证书以及打开页面
  **gitlab初次安装后，登录gitlab网页需要账号和密码**
  ```js
  // 查看gitlab登录账号root的密码
  cat /etc/gitlab/initial_root_password
  // 或者以下命令
  vi /etc/gitlab/initial_root_password
  ```
[!参考文章-本机虚拟机安装gitlab]https://blog.csdn.net/qq_42141141/article/details/126397059

# 八：k8s部署runner
  ### 1.安装helm3
    ```js
      https://github.com/helm/helm/releases
      tar -zxvf helm-v3.0.0-linux
      mv linux-amd64/helm /user/local/bin/helm
    ```
  ### 2.配置chart存储库
    ```js
      // 第1步：添加chart存储库
      helm repo add gitlab https://charts.gitlab.io
      // 第2步：验证源
      helm repo list
      // 第3步：查询可以安装的gitlab-runner chart
      helm search repo -l gitlab/gitlab-runner
    ```
  ### 3.更新配置信息
    ```js
      helm fetch gitlab/gitlab-runner --version=0.15.0
      [root@hahatuzi-service]# ls
      Desktop es
      Documents gitlab-runner-0.15.0.tgz
    ```

# 九：阿里云服务器部署node环境，因为yml脚本运行时用到了npm命令
  ### 1.下载安装
    ```js
      // 1. 执行以下命令，下载Node.js的安装包。
      wget https://npm.taobao.org/mirrors/node/v12.4.0/node-v12.4.0-linux-x64.tar.xz
      // 2. 执行以下命令，解压Node.js的安装包。
      tar -xvf node-v12.4.0-linux-x64.tar.xz
      // 3. 执行以下命令，重命名Node.js安装目录。
      mv node-v12.4.0-linux-x64/ /usr/local/node
    ```
  ### 2/.配置Node.js
    ```js
      // 1. 执行以下命令，将Node.js的可执行文件目录加入到系统环境变量中。
      echo "export PATH=$PATH:/usr/local/node/bin" >> /etc/profile
      // 2. 执行以下命令，使刚配置的Node.js环境变量立即生效。
      source /etc/profile
      // 3. 执行以下命令，分别查看node和npm版本。
      node -v
      npm -v
    ```
  ### 3.测试Node.js环境
    ```js
      // 1.使用vim命令创建一个测试文件。
      vim HelloWorld.js
      //  2. 输入i进入编辑模式。复制如下代码到HelloWorld.js文件中。
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
      // 按Esc键退出编辑模式，输入侧:wq保存退出。
      // 3.执行以下命令，运行HelloWorld.js文件。
      node HelloWorld.js
      // 4.打开浏览器，在地址范围输入http://<ECS公网地址>:8080，例如http://127.0.0.0:8080。如果返回如下界面，则表示成功。
    ```


# 十：静态服务器apache,或者nginx安装
  ### 第一步：检查是否有旧版本的apache
    rpm -qa | grep httpd 
  ### 第二步：安装
    yum -y install httpd
  ### 第三步：再次检查是否安装成功
    rpm -qa | grep httpd
  ### 第四步：启动apache,并修改端口号,因为gitlab服务可能占用了apache的默认端口80.
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
  ### 第五步：部署资源：每次pipeline的时候将本地机器代码远程拷贝到云服务器上
    sshpass -p $password scp -r ./build $custom_username@custom_ip:var/www/html
   - (1)需要在gitlab-ci.yml文件中添加
    ```js
      script: 
        - sshpass -p 812a1998D scp ./index.html root@47.99.144.3:/var/www/html
    ```
   - （2）在远程服务器上添加sshpass:
    ```js
      yum -y install sshpass
    ```
   - (3)关闭部署时报错Host key verification failed.
    ```js
      // 修改ssh——config文件中的 StrictHostKeyChecking为no
      vim /etc/ssh/ssh_config
    ```
  ### 第六步：创建远程域文件夹(可选)
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

  ### 注:Apache的默认配置文件路径：
   - （1）网站的根目录指向/var/www/html目录
   - (2)主配置文件时/etc/httpd/conf/httpd.conf
   - (3)存储在/etc/httpd/conf.d/目录
[!使用Docker Compose、Nginx、SSH和Github Actions实现前端自动化部署测试机]https://blog.csdn.net/qq_34998786/article/details/122227957?spm=1001.2014.3001.5502
  