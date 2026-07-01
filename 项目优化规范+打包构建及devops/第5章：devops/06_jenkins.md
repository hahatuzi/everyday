# jenkins

---

## 目录

1. [jenkins三大概念](#一、jenkins三大概念)
2. [jenkins插件](#二、jenkins插件)
3. [docker安装jenkins插件](#三、docker安装jenkins插件)
4. [jenkins流水线](#四、jenkins流水线)
5. [Jenkins常见的内置构建触发器](#五、Jenkins常见的内置构建触发器)
6. [jenkins配置](#六、jenkins配置)
7. [Jenkins安装](#七、Jenkins安装)
8. [jenkins权限管理](#八、jenkins权限管理)

---

## 一、jenkins三大概念
  ### 1.1 Job(任务)
  >在jenkins平台中，都是以job任务的形式完成一件事情。
  ### 1.2 plugins(插件)
  ### 1.3 workspace(工作空间)
  >jenkins是通过本地文件的形式来存储和管理数据的。jenkins下的每一个job都有属于自己的workspace,用来存放本任务涉及到的数据和文件
  >
---
## 二、jenkins插件
  ### 2.1 安装全局工具node
  安装nodejs插件 --> 安装全局工具node指定版本
---
## 三、jenkins项目构建
  ### 3.1 项目构建类型
  - (1)pipeline流水线类型
  > pipeline包括**声明式脚本**和**脚本式语法**，pipeline是一套运行在jenkins上的工作流框架，将原来独立运行于单个或者多个节点的任务连接起来，实现单个任务难以完成的复杂流程编排和可视化的工作。
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
    // 比如
    pipeline{
      agent  any
      stages {
          stage('拉取代码'){
              steps {
                  echo '拉取代码。。。'
              }
          }
          stage('制作镜像'){
              steps {
                  echo'制作镜像..'
              }
          }
          stage('部署') {
              steps {
                  echo'部署....'
              }
          }
      }
    }
    // 比如
    pipeline{
      agent any
      stages {
        stage('Checkout') {
          steps {
            git url: 'http://gitlab:8081/root/your-project.git',
              credentialsId: 'gitlab-credential',
              branch: 'main'
          }
        }
        stage('Build') {
          steps {
            sh 'npm install && npm run build'
          }
        }
        stage('Deploy to Nginx') {
          steps {
            sh '''
              rm -rf /var/jenkins_home/workspace/deploy/*
              cp -r dist/* /var/jenkins_home/workspace/deploy/
            '''
          }
        }
      }
    }
  ```
  [jenkins声明式语法](https://blog.csdn.net/zhou920786312/article/details/125955704)
  - (2)自由风格类型
---
  ### 3.2 常见的构建触发器
  > 构建触发器方式包括：**定时构建**，**远程构建**，**github触发器**，**源码变更构建**
  - (1)定时构建
    - 分钟(0-59)
    - 小时(0-24)
    - 每月的天数
    - 月数
    - 一周的天数(0-7)
    >比如：每天晚上20点自动构建：0 20 * * *,*表示取有效期的所有值，-表示连续的时间段  
    >每周二，周四的晚上8点执行 0 20 * * 2,4    
    >每周二至周四的晚上8点执行 0 20 * * 2-4  
  - (2)轮询SCM
  >定时扫描本地仓库的代码是否有边锋，如果代码有变更就会触发。  
  >轮询SCM可以实现Gitlab代码更新，项目自动构建，但是该方案的性能不佳，当项目代码量比较大时构建时间比较长。所以采用了更好的方案：利用Gitlab的webhook实现代码push到仓库时立即触发项目的自动构建
    - 示意图
    Jenkins  --发送定时请求-->  Gitlab代码变更 --> Gitlab代码变更  --push完毕后发送构建请求-->  Jenkins
---

## 六、jenkins配置
  ### 6.1 Jenkins全局变量
  - env  
    >env可以在声明式流水线中访问的环境变量，例如`${env.PATH}`或者`${env.BUILD_ID}`。访问内置的全局变量参考页面`${YOUR_JENKINS_URL}/pipeline-syntax/globals`以获取完整的最新的，可用于流水线的环境变量列表。
  - currentBuild  
    >currentBuild可用于发现当前正在执行的流水线的信息，比如result,displayName等属性。
  ### 6.2 Jenkins环境变量environment
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

---
## 七、Jenkins安装方式
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
  - 第六步：发布前端，转7.4
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
  ### 7.4 jenkins+nginx部署前端项目
  > Jenkins 的 deploy 路径是 /var/jenkins_home/workspace/deploy， Nginx 容器内的路径是/usr/share/nginx/html/，在 Jenkins 容器里不存在。  
  > Jenkins 和 Nginx 是两个独立容器，Jenkins 内部访问不到 /usr/share/nginx/html/，必须通过共享卷 web-data 来传递文件
  
  - 新建脚本npm run build,build后会在jenkins的安装目录下生成workspace工作空间，比如/usr/local/docker/jenkins/workspace/vue_low_code/dist
  - 将dist包copy到nginx目录下
  ```
  第一步：
    jenkins安装nodeJS插件
    新建任务
  第二步：
    方式一：宿主机环境部署jenkins和nginx都安装在宿主机环境中，jenkins的shell如下
      node -v
      npm -v
      npm install
      npm run build
      rm -rf /usr/share/nginx/html/vue_low_code/*
      cp -r dist/* /usr/share/nginx/html/vue_low_code/

    方式二：容器化部署：jenkins和nginx都作为docker容器，进行跨容器部署，jenkins的shell如下
      node -v
      npm -v
      npm install
      npm run build
      mkdir -p /var/jenkins_home/workspace/deploy/vue_low_code
      rm -rf /usr/share/nginx/html/vue_low_code/*
      cp -r dist/* /var/jenkins_home/workspace/deploy/vue_low_code/ # deploy/vue_low_code/（Jenkins 自动创建）
      echo "===== 部署完成，文件列表 ====="
      ls -la /var/jenkins_home/workspace/deploy/vue_low_code/
    方式三：dockerfile + docker compose方式部署
  第三步：docker.compose配置jenkins和nginx
    version: '3.8'
      services:
        jenkins:
          image: jenkins/jenkins:lts-jdk21
          container_name: jenkins
          restart: always
          ports:
            - "3000:8080"    # Web UI
            - "50000:50000"  # Agent 通信
          volumes:
            - ./jenkins_home:/var/jenkins_home
            - web-data:/var/jenkins_home/workspace/deploy
            - /var/run/docker.sock:/var/run/docker.sock   # 可选：Jenkins 内调用 Docker
          # environment:
          #       # JAVA_OPTS: "-Djenkins.install.runSetupWizard=false"
          user: root    # 解决 Docker socket 权限问题

        nginx:
          image: nginx:alpine
          container_name: nginx
          restart: always
          ports:
            - "8081:80"
          volumes:
            - web-data:/usr/share/nginx/html
          depends_on:
            - jenkins


      volumes:
        web-data:
  ```
  - 
  - 
---
## 八、jenkins权限管理
  >Role-based Authorization Strategy插件
  >全局安全配置 --> 授权策略 --> Role-based-Strategy --> Manage and Assign Roles --> Manage Roles
  ### 8.1 分类
  - 全局角色
  - 项目角色
  - 节点角色
  ### 8.2 jenkins凭证管理
  - ssh
  - 用户名和密码

## 九、Jenkins+Nginx容器化部署前端项目（命名卷方案）

  ### 9.1 架构概览
  ```
  GitHub
    │ git clone (SSH)
    ▼
  Jenkins 容器
    │ npm install → npm run build
    │ cp dist/* → /var/jenkins_home/workspace/deploy/vue_low_code/
    │                              │
    │                    ┌─────────┘
    ▼                    ▼
            ┌──────────────────┐
            │   web-data 命名卷  │  ← Docker 共享存储
            └────────┬─────────┘
                      │
                      ▼
  Nginx 容器
    │ 读取 /usr/share/nginx/html/vue_low_code/
    ▼
  用户浏览器 → http://服务器IP:80
  ```
---

  ## 9.2 第一步：目录结构
  ```
  ~/docker/
  ├── docker-compose.yml     # 自己mkdir
  ├── nginx/                 # 自己mkdir
  │   └── conf.d/            # 自己mkdir
  │       └── default.conf   # 自己mkdir
  ├── known_hosts
  ├── jenkins_home/          # 自动生成
  └── gitlab/                # 自动生成
  ```
---

  ### 9.3 第二步：docker-compose.yml
  ```bash
    version: '3.8'

    services:
      jenkins:
        image: jenkins/jenkins:lts-jdk21
        container_name: jenkins
        restart: always
        ports:
          - "9090:8080"
          - "50000:50000"
        volumes:
          - ./jenkins_home:/var/jenkins_home
          - /var/run/docker.sock:/var/run/docker.sock
          - web-data:/var/jenkins_home/workspace/deploy
          # - ./known_hosts:/var/jenkins_home/.ssh/known_hosts
        user: root

      nginx:
        image: nginx:alpine
        container_name: nginx
        restart: always
        ports:
          - "80:80"
        volumes:
          - ./nginx/conf.d:/etc/nginx/conf.d
          - web-data:/usr/share/nginx/html
        depends_on:
          - jenkins

    volumes:
      web-data:  # Docker 管理，实际路径 /var/lib/docker/volumes/项目名_web-data/_data
  ```
---

  ### 9.4 第三步：Nginx 配置
  ```bash
    cat > ~/docker/nginx/conf.d/default.conf << 'EOF'
    server {
        listen 80;
        server_name _;

        root /usr/share/nginx/html;
        index index.html;

        location /vue_low_code {
            alias /usr/share/nginx/html/vue_low_code;
            try_files $uri $uri/ /vue_low_code/index.html;
        }

        location ~* \.(js|css|png|jpg|svg|woff|woff2)$ {
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
    EOF
  ```
---

  ### 9.5 第四步：known_hosts（GitHub SSH）
  ```bash
  cat > ~/docker/known_hosts << 'EOF'
  github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
  github.com ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEmKSENjQEezOmxkZMy7opKgwFB9nkt5YRrYMjNuG5N87uRgg6CLrbo5wAdT/y6v0mKV0U2w0WZ2YB/++Tpockg=
  github.com ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCj7ndNxQowgcQnjshcLrqPEiiphnt+VTTvDP6mHBL9j1aNUkY4Ue1gvwnGLVgOhZoYrAvmYsac3ckxL8t5KzHxkFiW3T0P5GmOR3VWRMx0eqVRaoxUzR+F3DqDZ5yS7EnBBuJmQmPG5F1OjFH6wcx+F7pSz8VFvKsjZyfkVwMQPQ1CB5O6yBHLhqmiZK0DSv4A7gTZ1QvhnCHFgVb9wJWPJzM/+zFmy/RzFGQhMV5mANa1Z7bbTWX1Fuz3g/MQF6PRcvFNfkqhDmjlNXmmLdJ3q7S0HOm8yOvl9q3IqnV03BEF3E44fVKUoOxF6xXTQY0DBAkmXb8Qq9TV+E/XBRp1Em9FRf3ZqFFIM6AM3voxFQdFqRPQ9BPSfuG6YL0tLO/QPNN1n7d/jO+3jJ5tOJgvItz6z0a2MKWfmR4yZHlGsYjj0M0hDDaD5PyQw1RjzVZShhNOd9Z+x6YQ6N3C+jkZ0KZn6aIOd3KOo9Q/9s+m89vz/CBZWQRq+PXp6TI=
  EOF
  ```
---

  ### 9.6 第五步：启动容器
  ```bash
  cd ~/docker
  docker compose up -d
  ```
  查看状态：
  ```bash
  docker compose ps
  ```
---

  ### 9.7 第六步：配置 Jenkins SSH 密钥
  ```bash
  # 进入 Jenkins 容器生成密钥
  docker exec -it -u root jenkins bash
  # 生成 SSH 密钥（一路回车）
  ssh-keygen -t ed25519 -C "jenkins@docker" -f /var/jenkins_home/.ssh/id_ed25519
  # 查看公钥，复制到 GitHub → Settings → SSH and GPG keys → New SSH Key
  cat /var/jenkins_home/.ssh/id_ed25519.pub
  # 测试 GitHub 连接
  ssh -T git@github.com
  # 预期输出: Hi xxx! You've successfully authenticated...
  exit
  ```
---

  ### 9.8 第七步：获取 Jenkins 初始密码
  ```bash
  docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```
---

  ### 9.9 第八步：Jenkins 添加 GitHub SSH 凭据
   1. **Manage Jenkins** → **Credentials** → **System** → **Global credentials**
   2. 点击 **Add Credentials**
   3. 配置如下：

   | 字段 | 值 |
   |------|-----|
   | Kind | SSH Username with private key |
   | ID | `github-ssh-key` |
   | Username | `git` |
   | Private Key | 选择 **Enter directly** → 点击 **Add** |

   4. 获取私钥：

   ```bash
   docker exec jenkins cat /var/jenkins_home/.ssh/id_ed25519
   ```
    1. 将输出的内容（包括 `-----BEGIN OPENSSH PRIVATE KEY-----` 到 `-----END OPENSSH PRIVATE KEY-----`）完整粘贴
    2. 点击 **Create**
---

  ### 9.10 第九步：关闭 Git Host Key 严格检查（可选）
  如果 SSH 仍然报 host key 错误：
  1. **Manage Jenkins** → **Security** → **Git Host Key Verification Configuration**
  2. 选择 **`Accept first connection`** 或 **`No verification`**
  3. 保存
---

  ### 9.11 第十步：创建 Jenkins Pipeline 任务
   1. Jenkins 首页 → **新建任务** → 输入任务名 → 选择 **Pipeline** → 确定
   2. 在 Pipeline 配置中粘贴以下脚本：
   ```groovy
   pipeline {
       agent any

       environment {
           DEPLOY_PATH = '/var/jenkins_home/workspace/deploy/vue_low_code'
       }

       stages {

           stage('拉取代码') {
               steps {
                   git branch: 'main',
                       url: 'git@github.com:你的用户名/你的仓库.git',
                       credentialsId: 'github-ssh-key'
               }
           }

           stage('安装依赖') {
               steps {
                   sh 'npm install'
               }
           }

           stage('构建') {
               steps {
                   sh 'npm run build'
               }
           }

           stage('部署到 Nginx') {
               steps {
                   sh '''
                       echo ">>> 清空旧文件..."
                       rm -rf ${DEPLOY_PATH}/*

                       echo ">>> 创建目标目录..."
                       mkdir -p ${DEPLOY_PATH}

                       echo ">>> 拷贝构建产物到共享卷..."
                       cp -r dist/* ${DEPLOY_PATH}/

                       echo ">>> 部署完成！"
                       ls -la ${DEPLOY_PATH}/
                   '''
               }
           }
       }

       post {
           success {
               echo '✅ 部署成功！访问 http://服务器IP:80'
           }
           failure {
               echo '❌ 部署失败，检查日志'
           }
       }
   }
   ```

   3. 点击 **保存** → 点击 **Build Now** 执行构建
---
  ### 9.12 第十一步：验证部署
  ```bash
  # 查看 Jenkins 容器内的文件
  docker exec jenkins ls -la /var/jenkins_home/workspace/deploy/vue_low_code/

  # 查看 Nginx 容器内的文件（应该和上面完全一样）
  docker exec nginx ls -la /usr/share/nginx/html/vue_low_code/

  # 查看 index.html 内容
  docker exec nginx cat /usr/share/nginx/html/vue_low_code/index.html

  # 测试页面访问
  curl http://localhost

  # 浏览器访问
  # http://服务器IP:80
  ```
---

  ### 9.13 常见问题
  - 1.页面 404
```bash
# 检查写入文件
ocker exec jenkins ls -la /var/jenkins_home/workspace/deploy/vue_low_code/
# 检查文件是否存在
docker exec nginx ls -la /usr/share/nginx/html/vue_low_code/

# 如果目录为空，说明 Jenkins 构建未成功或拷贝路径不对
# 检查 Jenkins 构建日志中的部署阶段输出
```

  - 2. Nginx 容器端口冲突

```bash
# 查看端口占用
netstat -tlnp | grep 80

# 修改 docker-compose.yml 中 Nginx 端口，如改为 8088:80
```

  - 3. GitHub SSH 连接失败

```bash
# 手动添加 host key
docker exec -u root jenkins ssh-keyscan github.com >> /var/jenkins_home/.ssh/known_hosts

# 测试连接
docker exec jenkins ssh -T git@github.com
```

-  4. cp 报错 No such file or directory
> 执行顺序  
>  Jenkins 启动，自动创建 /var/jenkins_home/workspace/deploy/test/（在 jenkins_home 卷上）  
> Docker 挂载 web-data 空卷到该路径 → 把 Jenkins 自动创建的目录覆盖掉了  
> web-data 是空卷 → 路径变成空的 → cp 失败
```bash
# Jenkins Execute shell 中必须先创建目录
mkdir -p /var/jenkins_home/workspace/deploy/vue_low_code
rm -rf /var/jenkins_home/workspace/deploy/vue_low_code/*
cp -r dist/* /var/jenkins_home/workspace/deploy/vue_low_code/
```

  - 5. 重载 Nginx 配置

```bash
# 修改 nginx/conf.d/default.conf 后重载
docker exec nginx nginx -s reload

# 或者重启容器
docker compose restart nginx
```
  - 6.多项目部署，多个命名卷方式或者nginx多一级路径
  ```
    services:
      jenkins:
        image: jenkins/jenkins:lts-jdk21
        container_name: jenkins
        restart: always
        ports:
          - "9090:8080"
          - "50000:50000"
        volumes:
          - ./jenkins_home:/var/jenkins_home
          - /var/run/docker.sock:/var/run/docker.sock
          - web-data-test:/var/jenkins_home/workspace/deploy/test
          - web-data-prod:/var/jenkins_home/workspace/deploy/prod
          - web-data-demo:/var/jenkins_home/workspace/deploy/demo
        user: root

      nginx:
        image: nginx:alpine
        container_name: nginx
        restart: always
        ports:
          - "80:80"
        volumes:
          - ./nginx/conf.d:/etc/nginx/conf.d
          - web-data-test:/usr/share/nginx/html/test
          - web-data-prod:/usr/share/nginx/html/prod
          - web-data-demo:/usr/share/nginx/html/demo
        depends_on:
          - jenkins

    volumes:
      web-data-test:
      web-data-prod:
      web-data-demo:

  ```
---