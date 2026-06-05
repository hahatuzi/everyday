# Docker

# 一：Docker原理
  > 开始-->docker在本机寻找镜像-->判断本机是否存在镜像-->不存在就去Docker Hub上下载，找到并使用
  ## 1.docker为什么比VM快
  - docker有着比虚拟机更少的抽象层
  - docker利用的宿主机的内核，vm需要的是Guest OS
  - dcoker比虚拟机轻巧，核心环境只要4M
# 二:Docker优势：
  - 1.更快速的交付和部署：
    - 传统的需要一堆帮助文档，安装程序
    - docker：打包镜像发布测试，一键运行
  - 2.更便捷的升级和扩容缩容：
    - 项目打包成一个镜像，扩展到服务器A或者B
  - 3.更简单的系统运维：
    - 容器化之后，开发，测试环境都高度一致
  - 4.更高效的计算资源利用：
    - DOcker是内核级的虚拟化，一个物理机上可以运行很多的容器实例

# 三：核心概念
  ## 1.镜像：
    docker镜像就是一个模版，可以通过这个模版来创建容器服务！！tomcat镜像-->run-->tocat01容器
  ## 2.容器container:
    DOcker利用容器，独立运行一个或者一组应用，可以将容器理解为一个简易版的linux系统
  ## 3.仓库：
    仓库就是存放镜像的地方

# 四：Docker安装
  ## 1.安装包
  - yum install -y yum-utils
  ## 2.设置镜像仓库
  - yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo 
  ## 3.安装包
  -  yum install docker-ce docker-ce-cli containerd.io
  ## 4.启动docker
  - systemctl start docker
  ## 5.查看是否安装成功
  - docker --version
  ## 6.查看hello-world镜像
  - docker run hello-world
  ## 7.查看镜像
  - docker images
  ## 8.卸载docker
  - yum remove docker-ce docker-ce-cli containerd.io
  - rm -rf /var/lib/docker
  ## 阿里云镜像加速，也可以使用别的镜像
  -  sudo  mkdir -p /etc/docker
  ```js
    sudo  tee /etc/docker/daemon.jsn <<-'EOF' 
    {
      "registry-mirrors": ["https://qiyb9988.mirror.aliyuncs.com"]
    }
    EOF
    // 或者---------------
    sudo tee /etc/docker/daemon.json <<-'EOF'
    {
      "registry-mirrors": [
        "https://docker.xuanyuan.me",
        "https://docker.1ms.run",
        "https://docker.m.daocloud.io"
      ]
    }
    EOF

    sudo tee /etc/docker/daemon.json <<-'EOF'
    {
      "registry-mirrors": [
        "https://mirror.ccs.tencentyun.com",
        "https://docker.m.daocloud.io",
        "https://docker.nju.edu.cn"
      ]
    }
    EOF
  ```
  - sudo systemctl daemon-reload
  - sudo systemctl restart docker

# 五：Docker Compose
  ## 1.概念
   - dockerCOmpose是用来定义和运行一个或者多个容器的工具，现在无需安装
  ## 2.命令
    - docker compose up,启动
    - docker compose down,下线
    - docker compose version
    - docker compose -f compose.yaml up -d
  ## 3.元素
    - command：覆盖容器启动后的命令
    - environment：指定环境变量
    - image:指定镜像
    - networks:指定网络
    - ports：指定要发布的端口
    - volumes：指定数据卷
    - restart：指定重启策略
  ## 3.文件实例：
    ```js
      name: myblog
      services:
        mysql:
        image: mysql:8.0
        ports:
          - "3306:3306"
        environment:
          - MYSQL_ROOT_PASSWORD=XXX
          - MYSQL_DATABASE=wordpress
        volumes:
          - mysql-data:/var/lib/mysql
          - /app/myconf:/etc/mysql/conf.d
        restart:always
        networks:
          - blog

      workpress:
        image:wordpress
        ports:
          - "8080:80"
        environment:
          WORKPRESS_DB_HOST:mysql
          WORKPRESS_DB_USER:XXX
          WORKPRESS_DB_PASSWORD:XXX
          WORKPRESS_DB_NAME:workpress
        volumes:
          - wordpress:/var/www/html
        restart:always
        networks:
          - blog
        depends_on:
          - mysql
      volumes:
        mysql:
        wordpress:
      networks:
      blog:
    ```

# 六：Docker命令
  - docker ps [命令]:查看当前docker在跑哪些容器进程
  - docker container ls
  - docker container ls -a:查看所有的容器
  - docker images,查看镜像
  - docker run --name miaoma-nginx-server -d -p 8080:80 nginx
  - docker search:搜索，比如docker search mysql
  - docker pull [镜像名],下载镜像，比如docker pull mysql
  - docker rmi -f 容器id,删除指定容器,docker rm -f everyday
  - docker rmi -f 容器id 容器id 容器id,删除多个容器
  - docker rmi -f $(docker images -aq),删除所有容器
  - docker run [可选参数] images,新建容器并启动
  - docker run -it centos /bin/bash,测试，启动并进入容器
  - exit,退出容器到主机
  - docker run -d 镜像名，后台启动容器，docker run -d centos
  - docker start，启动
  - docker logs --help，查看日志
  - docker inspect [镜像id],查看镜像元数据
  - docker cp 容器id,拷贝
  - docker stop [镜像id],停止镜像
  - -d:后台运行
  - -p 端口1：端口2,端口映射，比如docker run -it -d -p 3310:3306 -v /home/mysql/conf.d -v /home/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=812a1998D --name hahatuzi mysql
  - -v，卷挂载
  - -e,环境配置
  - --name,容器名字
  - docker exec,进入
  - docker exec -it [镜像名] /bin/bash,进入镜像,或者docker attach [容器id],attach不会启动新的进程,exec进入容器后开启一个新的终端，可以直接操作
  - docker exec my-frontend ls /usr/share/nginx/html，检查挂载是否生效
  - docker exec my-frontend nginx -t，检查配置文件是否正确
  - docker logs my-frontend，查看错误日志
  - docker exec my-frontend cat /etc/nginx/conf.d/default.conf，查看Nginx实际使用的配置

# 七：docker镜像加载原理
  ## UnionFS（联合文件系统）
  - UnionFS是一层一层的文件系统，包含boot fs(boot)和root fs，它支持对文件系统的修改，作为一次提交来层层叠加
  - Union文件系统是Docker镜像的基础，在下载镜像的时候，已经存在的文件部分可以复用
  - root fs在boot fs之上，包含的就是典型的linux系统中的/dev,/proc,/bin,/etc等标准目录和文件
  ## 镜像的特点：
  - docker镜像都是只读的，当容器启动的时候，一个新的可写层被加载到镜像的顶部，这一层就是通常说的容器层，容器之下都是镜像层
# 八：提交镜像docker commit:
  ## 实战：将tomcat从webapps/dist中copy到webapps下


# 九：容器数据卷： -v
  > 正常情况下，容器删除时容器内的数据也会丢失，我们希望的就是Docker容器内的数据同步到本地，这就是容器卷
  ## 1.使用方式：
  ### (1)方式一:挂载在宿主机目录：docker run -it -v 主机目录，容器内目录
    ```js
      // 前端挂载在宿主机
      -v D:/my-project/dist:/usr/share/nginx/html
      // centos挂载在宿主机
      cd /home //进入服务器的home目录
      docker run -it -v /home/test:/home centos
    ```
  ### (2)方式二:挂载在数据卷目录： named volume
    ```js
      // 前端挂载在数据卷目录
      -v frontend-data:/usr/share/nginx/html
    ```
  ### (3)方式三：匿名卷
    ```js
      // 前端挂载在数据卷目录
      -v /usr/share/nginx/html
    ```
  ## 2.实战：mysql数据持久化问题
    ```js
      docker run -it -d -p 3310:3306 -v /home/mysql/conf.d -v /home/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=自己的密码 --name 自己的名字 mysql
      // sqlyog连接到服务器3310
      cd /home/mysql/data
      ls
    ```
  ## 3.具名挂载和匿名挂载
  ### (1)匿名挂载：-v只写了容器内的路径，没有写容器外的路径
  ### (2)具名挂载
  docker run -d -P --name nginx02 -v jumming-nginx:/etc/nginx nginx
  ## 4.命令：
  - docker run -v 数据卷别名:容器目录 镜像名，设置数据卷
  - docker volume ls,查看所有数据卷
  - docker volume inspect 数据卷名,查看数据卷详情
  - docker volume create数据卷名,创建数据卷
  - docker volume rm 数据卷名，删除数据卷

# 十：Dockerfile
  > dockerfile就是构建docker镜像的文件
  ## 1.创建dockerfile文件：
  - cd /home
  - mkdir docker-test-volume
  - cd docker-test-volume
  - vim dockerfile ，在docker-test-volume文件夹下创建dockerfile文件
  - cat dockerfile
  - docker build -f dockerfile -t /hahatuzi/centos:1.0 . ，根据dockerfile生成一个镜像,.!!!不能忘记.
  - docker run -it --name docker02 --volumes-from docker01 hahatuzi/centos:1.0
  ## 2.dockerfile的构建过程
  - 构建过程中关键字必须是大写
  - 从上到下执行
  - 每一个指令都会创建提交一个新的镜像层，并提交
  ## 3.dockerfile的指令
  - FROM:镜像使用的基础镜像，docker官网有node可以使用镜像列表
  - MAINTAINER:维护人信息
  - RUM:运行命令
  - ADD:COPY文件，会自动解压
  - WORKDIR:设置当前工作目录
  - VOLUME:设置卷，挂载主机目录
  - EXPOSE:保留端口配置
  - CMD:指定容器启动的时候要运行的命令，只有最后一个会生效，可被替代
  - ENTERPOINT:指定容器启动的时候要运行的命令,可以追加命令
  - ONBUILD:当构建一个被继承Dockerfile这个时候就会运行ONBUILD的指令，触发指令
  - COPY:类似ADD,将文件拷贝到镜像中
  - ENV:构建的时候设置环境变量
  ## 4.创建自己的centos
  - 创建自己的dockerfile
  - docker build -f dockerfile -t mycentos:0.1 . ，dockerfile为自己创建的dockerfile文件名
  - 
  ## 5.CMD和ENTERPOINT的区别

# 十一：实例：
  ## 1.nginx安装
  ```js
    // docker pull nginx
    // docker images
    // docker run -d --name nginx01 -p 8888:80 nginx
    // docker exec -it nginx01 /bin/bash
    // docker ps
    // docker stop 51f5b9d0c0f8
    // curl localhost:8888
  ```
  ## 2.tomcat安装
  ```js
    // docker pull tomcat
    // docker images
    // docker run -d --name tomcat01 -p 3389:80 tomcat
    // docker exec -it tomcat01 /bin/bash
    // cd webapps
    // ls，发现tomcat是阉割版本
    // cp -r webapps.dist/* webapps
  ```
  ## 3.部署ES+Kibana
  ## 4.Dockerfile制作tomcat镜像
    ```js
      FROM centos
      MAINTAINENT hahatuzi
      COPY readme.txt /usr/local/readme.txt
      ADD jdk-8ull-linux-x64.tar.gz /usr/local/
      ADD apache-tomcat-9.0.22.tar.gz /usr/local/
      RUN yum -y install vim
      ENV MYPATH /usr/local
      WORKDIR $MYPATH

      ENV JAVA_HOME /usr/local/jdk1.8.0_11
      ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
      ENV CATALINA_HOME /usr/local/apache-tomcat-9.0.22
      ENV CATALINA_BASH /usr/local/apache-tomcat-9.0.22
      ENV PATH $PATH:$JAVA_HOME/bin:$CATALINE_HOME/lib:$CATALINE_HOME/bin

      EXPOSE 8080
      CMD /usr/local/apache-tomcat-9.0.22/bin/startup.sh && tail -F /usr/local/apache-tomcat-9.0.22/bin/logs/cataline.out
    ```
    - 编写dockerfile，内容如上
    - 构建镜像：docker build -t diytomcat .
    - docker run -d -p 9090:8080 --name hahatuzitomcat -v /home/hahatuzi/build/tomcat/test:/usr/local/apache-tomcat-9.0.22/webapps/test -v /home/hahatuzi/build/tomcat/tomcatlogs/:/usr/local/apache-tomcat-9.0.22/logs diytomcat
    - docker exec -it 镜像id /bin/bash
    - 发布项目，由于做了卷挂载，我们直接在本地编写项目就可以发布了，cd test
    - mkdir WEB-INF
    - cd WEB-INF/
    - vim web.xml
# 十二：发布镜像：
  ## 1.发布自己的镜像到dockerhub：
  - 第一步：dockerhub上注册账号
  - 第二步：在我们的服务器上提交自己的镜像，docker login -u hahatuzi
  - 第三步：提交惊喜那个，尽量带上版本号和作者信息，docker push hahatuzi/diytomcat:1.0
  ## 2.发布到阿里云容器服务
  - 第一步：在阿里云上创建**命名空间**和**容器镜像**

# 十三：docker容器
  ## docker是如何处理容器网络访问的？
  - docker network create XXX,创建网络
  - docker network ls:列出网络
  - docker run --network 网络名 镜像名，加入网络
  - docker netwoek connect 网络名 容器名，创建后新加网络
  - docker network inspect网络名/id，查看网络详情
  - docker network inspect 网络名/id,删除网络
  - docker run -d -P --name tomcat01 tomcat
  - docker exec -it tomcat ip addr
  - tomcat01和tomcat02是公用的一个路由器docker0,docker会给你一个容器分配一个ip


# Docker可视化管理工具:portainer
# 思考：每次修改nginx配置文件，都要进入容器内部，能不能在容器外部提供一个映射路径，达到修改它的时候，容器内部自动修改的目的？
# dockerfile文件解读
    ```js
      // 第一步：指定镜像
      FROM XXX // docker官网有node可以使用镜像列表
      // 第二步：指定工作区
      WORKDIR /application
      // 第三步：将自己打包后的产物都copy到application工作区下
      COPY ..
      RUN npm install
      EXPOSE 3000
      CMD ['npm', 'start']

      // docker build -t XXX
      // docker run -d --name XXX
      // 举例：
      FROM nginx:apline
      COPY /dist /user/share/nginx/html
      EXPOSE 80
    ```

  ### docker swarm
  - docker swarm init --advertise-addr 172.24.82.149

# docker部署前端实例：
  ## 1.方式一：开发本地打包 + docker run：前端页面文件放在宿主机上，通过 Docker 挂载给 Nginx 容器
  - 第一步:开发本地打包
  - 第二步：配置nginx
  - 第三步：docker run 容器运行，docker run -p 8888:80 -v /usr/web/everyday/dist:/usr/share/nginx/html/everyday_doc --restart always -d --name everyday nginx
    - 前端页面宿主机地址：/usr/web/everyday/dist
    - Docker 挂载给 Nginx 容器/usr/share/nginx/html/everyday_doc
  ## 1.方式一：只用 Dockerfile（单服务）
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────┐
  │  前端源码   │ →   │  Dockerfile │ →   │  docker     │ →   │  docker  │
  │             │     │  构建定义   │     │  build      │     │  run     │
  └─────────────┘     └─────────────┘     └─────────────┘     └──────────┘
  - docker build -t everyday .
  - docker run -d -p 8888:80 everyday
  ## 2.方式二：Dockerfile + Docker Compose（推荐）
  Dockerfile + docker-compose.yml → docker compose up -d --build
  ## 3.方式三：只用 Docker Compose（用现成镜像）
  docker-compose.yml（全部用 image，不写 build）→ docker compose up
  ## 4.方式四：Docker Compose 构建推送到仓库
  docker compose build → docker compose push
  

  