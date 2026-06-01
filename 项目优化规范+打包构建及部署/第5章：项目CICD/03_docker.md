# Docker
# 一：历史：dcoker比虚拟机轻巧，核心环境只要4M
# 二优势：
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
  ## 8卸载docker
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
  ```
  - sudo systemctl daemon-reload
  - sudo systemctl restart docker

# 五：Docker原理
  > 开始-->docker在本机寻找镜像-->判断本机是否存在镜像-->不存在就去Docker Hub上下载，找到并使用
  ## 1.docker为什么比VM快
  - docker有着比虚拟机更少的抽象层
  - docker利用的宿主机的内核，vm需要的是Guest OS
# 六：Docker命令
  - docker ps [命令]:查看当前docker在跑哪些容器进程
  - docker container ls
  - docker container ls -a:查看所有的容器
  - docker images查看镜像
  - docker run --name miaoma-nginx-server -d -p 8080:80 nginx
  - docker search:搜索，比如docker search mysql
  - docker pull [镜像名],下载镜像，比如docker pull mysql
  - docker rmi -f 容器id,删除指定容器
  - docker rmi -f 容器id 容器id 容器id,删除多个容器
  - docker rmi -f $(docker images -aq),删除所有容器
  - docker run [可选参数] images,新建容器并启动
  - docker run -it centos /bin/bash,测试，启动并进入容器
  - exit,退出容器到主机
  - docker run -d 镜像名，后台启动容器，docker run -d centos
  - docker logs --help，查看日志
  - docker inspect [镜像id],查看镜像元数据
  - docker exec -it [镜像名] /bin/bash,进入镜像,或者docker attach [容器id],attach不会启动新的进程,exec进入容器后开启一个新的终端，可以直接操作
  - docker cp 容器id,拷贝
  - docker stop [镜像id],停止镜像

# 七：docker镜像加载原理
  ## UnionFS（联合文件系统）
  - UnionFS是一层一层的文件系统，包含boot fs(boot)和root fs，它支持对文件系统的修改，作为一次提交来层层叠加
  - Union文件系统是Docker镜像的基础，在下载镜像的时候，已经存在的文件部分可以复用
  - root fs在boot fs之上，包含的就是典型的linux系统中的/dev,/proc,/bin,/etc等标准目录和文件
  ## 镜像的特点：
  - docker镜像都是只读的，当容器启动的时候，一个新的可写层被加载到镜像的顶部，这一层就是通常说的容器层，容器之下都是镜像层



# 思考：每次修改nginx配置文件，都要进入容器内部，能不能在容器外部提供一个映射路径，达到修改它的时候，容器内部自动修改的目的？
# Docker可视化管理工具:portainer
# 实例：
  ## nginx安装
  ```js
    // docker pull nginx
    // docker images
    // docker run -d --name nginx01 -p 8888:80 nginx
    // docker exec -it nginx01 /bin/bash
    // docker ps
    // docker stop 51f5b9d0c0f8
    // curl localhost:8888
  ```
  ## tomcat安装
  ```js
    // docker pull tomcat
    // docker images
    // docker run -d --name tomcat01 -p 3389:80 tomcat
    // docker exec -it tomcat01 /bin/bash
    // cd webapps
    // ls，发现tomcat是阉割版本
  ```
  ## 部署ES+Kibana
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
  ### docker compose服务编排
    - 前端静态资源托管服务，nginx
    - 服务端服务。node,pm3
    - 基础服务redis,postgresql
  ```js
  version '3.8'
  include:
   - ./docker-compose.infra.yml
   services:
    frontend:
    build:
    context:./frontend
    ports:
    -"5173:80"
    networks:
    app-network
  ```