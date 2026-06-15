# jenkins

---

## 目录

1. [jenkins三大概念](#一、jenkins三大概念)
2. [jenkins创建job](#二、jenkins创建job)
3. [集群安装](#三、集群安装)
4. [node](#四node)
5. [NameSpace](#五NameSpace)
6. [Pod](#六Pod)
7. [Controller](#七Controller)
8. [Service](#八Service)
9. [Label](#九Label)

---

## 一、jenkins三大概念
  ### 1.1 Job(任务)
  >在jenkins平台中，都是以job任务的形式完成一件事情。
  ### 1.2 plugins(插件)
  ### 1.3 workspace(工作空间)
  >jenkins是通过本地文件的形式来存储和管理数据的。jenkins下的每一个job都有属于自己的workspace,用来存放本任务涉及到的数据和文件
## 二、jenkins创建job

## 三、docker安装jenkins插件
  - docker pull jenkins/jenkins
## 四、jenkins pipeline
  > pipeline包括声明式脚本和脚本式语法，pipeline是一套运行在jenkins上的工作流框架，将原来独立运行于单个或者多个节点的任务连接起来，实现单个任务难以完成的复杂流程编排和可视化的工作。
  - 声明式：
  ```js
    pipeline{ // 声明
      agent //'在哪个节点上构建',
      stages:{
        // 阶段，包含所有的任务步骤
        stage("scan"){
          steps{
            // 步骤，具体的任务步骤
          }
        }
      }
      post{
        // 任务完成之后的处理，比如发送邮件等
      }
    }
  ```
agent:代理
stages：阶段
checkout阶段
shell编译阶段
[jenkins声明式语法](https://blog.csdn.net/zhou920786312/article/details/125955704)
## 五、Jenkins的常见的内置构建触发器
  > 构建触发器：构件方式包括：**定时构建**，**远程构建**，**github触发器**，**源码变更构建**
  - **定时构建**:分类包括：分钟(0-59)，小时(0-24)，每月的天数，月数，一周的天数(0-7)
比如：每天晚上20点自动构建：0 20 * * *,*表示取有效期的所有值，-表示连续的时间段
每周二，周四的晚上8点执行 0 20 * * 2,4
每周二至周四的晚上8点执行 0 20 * * 2-4
  - **轮询SCM**:定时扫描本地仓库的代码是否有边锋，如果代码有变更就会触发
轮询SCM可以实现Gitlab代码更新，项目自动构建，但是该方案的性能不佳，当项目代码量比较大时构建时间比较长。所以采用了更好的方案：利用Gitlab的webhook实现代码push到仓库时立即触发项目的自动构建
轮询SCM原理示意图
Jenkins  --发送定时请求-->  Gitlab代码变更
Gitlab代码变更  --push完毕后发送构建请求-->  Jenkins
## 六、Jenkins全局变量
  - env  
  env可以在声明式流水线中访问的环境变量，例如`${env.PATH}`或者`${env.BUILD_ID}`.
访问内置的全局变量参考页面`${YOUR_JENKINS_URL}/pipeline-syntax/globals`以获取完整的最新的，可用于流水线的环境变量列表。
  - currentBuild  
    currentBuild可用于发现当前正在执行的流水线的信息，比如result,displayName等属性。
## 七、Jenkins环境变量environment
  - (1)最外层，用在最外层的pipeline块中的enviroment指令用于流水线的所有步骤
  - (2)stage中，定义在stage中的enviorment指令只适用于stage中的步骤。
  ```
  pipeline{
    enviorment{

    }
    stages{
      stage(){
        environment{

        }
      }
    }
  }
  ```

## 七、Jenkins安装
  ### 7.1 linux直接安装
  ```
  第一步：安装jdk
  第二步：
    sudo wget -0 /etc/yum.repos.d/jenkins.repo \ https://pkg.jenkins.io/redhat-stable/jenkins.repo
  第三步：
    sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
  第四步：
    sudo yum upgrade
  第五步：为jenkins包添加所需的依赖项
    sudo yum install fontconfig
  第六步：
    sudo yum install jenkins
  第七步：启动jenkins
    sudo systemctl daemon-reload
    或者：
    sudo systemctl enable jenkins
    或者：
    sudo systemctl start jenkins
  检查jenkins状态
    sudo systemctl status jenkins
  ```
---
  ### 7.2 docker安装jenkins容器
  - 第一步：创建jenkins目录，可以参考：/usr/local/docker/jenkins/docker-compose.yml
  ```
    mkdir -p ~/jenkins && cd ~/jenkins
  ```
  - 第二步：创建 docker-compose.yml
  ```
    version: '3.8'

    services:
      jenkins:
        image: jenkins/jenkins:lts-jdk17
        container_name: jenkins
        restart: always
        ports:
          - "8080:8080"    # Web UI
          - "50000:50000"  # Agent 通信
        volumes:
          - ./jenkins_home:/var/jenkins_home
          - /var/run/docker.sock:/var/run/docker.sock   # 可选：Jenkins 内调用 Docker
        environment:
          JAVA_OPTS: "-Djenkins.install.runSetupWizard=false"
        user: root    # 解决 Docker socket 权限问题
  ```
  - 第三步：启动
  ```
    docker compose up -d
  ```
  - 第四步：查看日志获取初始密码
  ```
    docker logs -f jenkins
    docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```
  - 第五步：如果看不到密码？？就把第二步中JAVA_OPTS注释掉，该行的意思是跳过安装向导，不生成密码文件
  ```
    JAVA_OPTS注释掉
    docker compose down
    rm -rf jenkins_home // 删掉旧数据
    docker compose up -d
    sleep 30
    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```
---
  ### 7.3 Jenkins + GitLab 同机部署（端口不冲突）
  - 配置文件
  - docker run -d --name jenkins --restart always -p 8080:8080 -p 50000:50000 -v ~/jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -u root jenkins/jenkins:lts-jdk17
  ```
    version: '3.8'

    services:
      gitlab:
        image: gitlab/gitlab-ce:latest
        container_name: gitlab
        hostname: gitlab.local
        restart: always
        ports:
          - "8081:80"
          - "2222:22"
        volumes:
          - ./gitlab/config:/etc/gitlab
          - ./gitlab/logs:/var/log/gitlab
          - ./gitlab/data:/var/opt/gitlab
        environment:
          GITLAB_OMNIBUS_CONFIG: |
            external_url 'http://gitlab.local:8081'
            gitlab_rails['gitlab_shell_ssh_port'] = 2222
        mem_limit: 4096m

      gitlab-runner:
        image: gitlab/gitlab-runner:latest
        container_name: gitlab-runner
        restart: always
        volumes:
          - ./runner/config:/etc/gitlab-runner
          - /var/run/docker.sock:/var/run/docker.sock
        depends_on:
          - gitlab

      jenkins:
        image: jenkins/jenkins:lts-jdk17
        container_name: jenkins
        restart: always
        ports:
          - "9090:8080"
          - "50000:50000"
        volumes:
          - ./jenkins_home:/var/jenkins_home
          - /var/run/docker.sock:/var/run/docker.sock
        user: root
  ```
  ### 7.4 jenkins部署前端项目
  - jenkins安装nodeJS插件