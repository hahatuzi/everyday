# gitlab CICD

---

## 目录

1. [gitlab CICD](#一、gitlab_CICD)
2. [gitlab安装及使用](#二、gitlab安装及使用)
3. [gitlab runner的安装与使用](#三、gitlab runner的安装与使用)
4. [pipeline语法](#四、pipeline语法)
5. [NameSpace](#五NameSpace)
6. [Pod](#六Pod)
7. [Controller](#七Controller)
8. [Service](#八Service)
9. [Label](#九Label)

---


## 一、gitlab_CICD
  ### 1.1 组成
  - gitlab:代码托管平台,就像 GitHub 网站
  - gitlab runner:	CI/CD 执行器,	必须连接 GitLab 才能用,	可选（不用 CI/CD 就不装）,就像 Jenkins Agent
  - gitlab-ci.yml
  > **Runner 可以和 GitLab 装在同一台机器，也可以装在另一台。也可以在同一个主机上设置多个gitlab-runner ,还可以根据不同的环境设置不同的环境，比如我们需要区分研发环境，测试环境以及正式环境等。**
---
  ### 1.2 工作流程
  ```
  ──→ 1.代码托管到git仓库
  ──→ 2.项目根目录创建ci文件,gitlab-ci.yml,在文件中指定构建，测试和部署脚本
  ──→ 3.gitlab检测到gitlab-ci.yml并使用gitlab runner 的工具运行脚本
  ──→ 4.根据预定义的gitlab-ci.yml脚本分组成作业，并共同组成管道
  你 项目添加gitlab-ci.yml文件，然后git push 代码
       ↓
  ┌─────────┐
  │ GitLab  │  ← 收到代码，触发 CI/CD 流水线
  └────┬────┘
       │ 发送任务
       ↓
  ┌──────────────┐
  │ GitLab Runner│  ← 接到任务，根据预定义的gitlab-ci.yml脚本分组成作业，并共同组成管道，执行构建/测试/部署
  └──────────────┘
  ```
---
  ### 1.3 gitlab CI/CD的特点
  - 1.多平台
  - 2.多语言
  - 3.稳定构建：构建与gitlab在不同的机器上运行
  - 4.并行构建：gitlab CI/CD在多态机器上拆分构建，从而实现快速执行
  - 5.实时日志记录
  - 6.灵活的管道
  - 7.版本管道：一个gitlab-ci.yml文件包含测试，整个过程的步骤
---
  ### 1.4 gitlab CI的完整流程
  - 第一步：阿里云服务器安装gitlab
  - 第二步：阿里云服务器安装gitlab-runner
  - 第三步：将本地推送到gitlab并自动部署
---
  ### 1.5 前端pipeline中需要的操作
  - 第一步：install阶段：就是执行npm install 命令，根据package.json安装node_modules依赖包
  - 第二步：eslint阶段: 执行eslint检查，判断代码格式是否符合规范，如果不符合停止pipeline
  - 第三步：build阶段: 编译成生产代码，可以通过webpack之类的打包工具执行编译，也可以通过脚手架自身提供的编译命令进行编译,如npm run build
  - 第四步：deploy阶段：部署阶段，将刚才的build阶端生成的生产代码部署到生产访问的服务器上，
---

## 二、gitlab安装及使用
  ### 2.1 安装方式一：使用rpm包安装
    ```js
      // 第一步：安装依赖
      sudo dnf install -y curl policycoreutils openssh-server openssh-clients postfix
      // 启动 postfix
      sudo systemctl enable postfix
      sudo systemctl start postfix
      // 第二步：使用清华大学镜像下载16.11.0版本的gitlab,因为4核服务器跑不动最新版本的gitlab
      wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el9/gitlab-ce-16.11.0-ce.0.el9.x86_64.rpm
      // 第三步：应用配置（首次安装会自动执行）
      sudo gitlab-ctl reconfigure
      // 第四步：查看服务状态
      sudo gitlab-ctl status
      // 重启
      sudo gitlab-ctl restart
      // 获取初始 root 密码
      sudo cat /etc/gitlab/initial_root_password
      // 编辑站点地址，修改external_url和listen_port
      sudo vi /etc/gitlab/gitlab.rb
      # 查看内存占用
      sudo gitlab-ctl status
      free -h
      # 查看各组件内存占用
      ps aux --sort=-%mem | grep -E 'puma|sidekiq|postgres|redis|gitaly|nginx' | awk '{print $2, $4, $6, $11}' | head -10
    ```
  ### 2.2 安装方式二：使用docker安装
    ```js
      第一步：创建目录
        cd /usr/local
        mkdir docker
        mkdir gitlab_docker
        vim docker-compose.yml
      第二步：搜索gitblab镜像
        docker search gitlab 
      第三步：拉取镜像
        docker pull gitlab/gitlab-ce:latest
      第四步：配置docker-compose.yml文件,关闭gitlab所有监控组件
        version: '3.1'
        services:
          gitlab:
            image: gitlab/gitlab-ce:latest
            container_name: gitlab
            restart: always
            environment:
              GITLAB_OMNIBUS_CONFIG:
                external_url 'http://192.168.11.11:8929' // 自己的服务器ip
                gitlab_rails[' gitlab_shell_ssh_port' ] = 2224
                external_url 'http://你的IP';
                prometheus_monitoring['enable'] = false;
                alertmanager['enable'] = false;
                node_exporter['enable'] = false;
                grafana['enable'] = false;
                puma['worker_processes'] = 2;
                puma['min_threads'] = 1;
                puma['max_threads'] = 2;
                sidekiq['max_concurrency'] = 5;
                postgresql['shared_buffers'] = '128MB';
                postgresql['max_worker_processes'] = 2;
                nginx['worker_processes'] = 1;
                gitlab_rails['backup_keep_time'] = 604800;
            ports:
              - '8929:8929'
              - '2224:2224'
            volumes:
              - './config:/etc/gitlab'
              - './logs:/var/log/gitlab'
              -  './data:/var/opt/gitlab'
      第五步：启动容器
        docker-compose up -d
    ```
  ### 2.3 gitlab常见命令
    ```
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
  ### 2.4 gitlab安装的前置条件，可不做！！
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
  ### 2.5 gitlab配置优化，用来优化服务器占用太高
  ```js
      # ========== 外部访问地址 ==========
      external_url 'http://gitlab.example.com'

      # ========== 时区 ==========
      gitlab_rails['time_zone'] = 'Asia/Shanghai'

      # ========== 关闭所有非必要组件（省内存）==========
      prometheus_monitoring['enable'] = false
      alertmanager['enable'] = false
      node_exporter['enable'] = false
      grafana['enable'] = false
      gitlab_exporter['enable'] = false
      redis_exporter['enable'] = false
      postgres_exporter['enable'] = false
      gitlab_kas['enable'] = false
      gitlab_pages['enable'] = false
      registry['enable'] = false
      mattermost['enable'] = false
      mailroom['enable'] = false

      # ========== Puma 优化（Web 应用服务器）==========
      puma['worker_processes'] = 2          # 2个worker，不能再少
      puma['min_threads'] = 1               # 最小线程
      puma['max_threads'] = 2               # 最大线程（限制并发）
      puma['worker_timeout'] = 60
      puma['per_worker_max_memory_mb'] = 300  # 每个worker最大300MB

      # ========== Sidekiq 优化（后台任务）==========
      sidekiq['max_concurrency'] = 5        # 最大并发（默认25）
      sidekiq['min_concurrency'] = 1        # 最小并发
      sidekiq['timeout'] = 30
      sidekiq['memory_killer'] = true       # 内存过高自动重启
      sidekiq['memory_killer_max_memory_gc'] = '200000'  # 200MB触发GC

      # ========== PostgreSQL 优化 ==========
      postgresql['shared_buffers'] = '128MB'    # 共享缓存（默认256MB）
      postgresql['max_worker_processes'] = 2    # 最大工作进程（默认8）
      postgresql['work_mem'] = '8MB'            # 工作内存
      postgresql['maintenance_work_mem'] = '32MB'
      postgresql['effective_cache_size'] = '512MB'
      postgresql['checkpoint_timeout'] = '15min'
      postgresql['wal_buffers'] = '4MB'
      postgresql['max_connections'] = 50        # 最大连接数（默认200）
      postgresql['shared_preload_libraries'] = ''  # 关闭扩展

      # ========== Redis 优化 ==========
      redis['maxmemory'] = '64MB'
      redis['maxmemory_policy'] = 'allkeys-lru'

      # ========== Gitaly 优化 ==========
      gitaly['concurrency'] = [
        { 'section' => 'cat-file', 'workers' => 10 },
        { 'section' => 'gitaly2', 'workers' => 2 },
        { 'section' => 'pack_objects', 'workers' => 2 },
        { 'section' => 'repack', 'workers' => 1 }
      ]
      gitaly['ruby_max_rss'] = '200000000'      # 200MB
      gitaly['graceful_restart_timeout'] = '1m'

      # ========== Nginx 优化 ==========
      nginx['worker_processes'] = 1
      nginx['worker_connections'] = 512
      nginx['keepalive_timeout'] = 30

      # ========== 日志优化（减少磁盘IO）==========
      logging['logrotate_frequency'] = 'daily'
      logging['logrotate_size'] = '50M'
      logging['logrotate_keep'] = 3

      # ========== 备份 ==========
      gitlab_rails['backup_keep_time'] = 604800  # 保留7天

  ```
---

## 三、gitlab runner的安装与使用
  支持运行在目前常用的平台上，例如：Linux/Unix、Windows、MacOS、Docker容器内、Kubernetes。
  ### 3.1 概念
   - (1)gitlab Runner是一个开源项目，用于运行作业并将结果发送回gitlab。
   - (2)与gitlab CI结合使用，容器部署需要使用docker，gitlab runner版本应该和gitlab版本同步。
   - (3)可以根据需要配置任意数量的runner
   - (4)gitlab runner类似于jenkins的agent,执行CI持续集成，持续构建的脚本任务。
---
  ### 3.2 特点
  - (1)作业运行控制：同时执行多个作业
  - (2)作业运行环境：在本地使用docker容器，使用docker容器并通过SSH执行作业。
  - (3)允许自定义作业运行环境
  - (4)支持运行在目前常用的平台上，例如：Linux/Unix、Windows、MacOS、Docker容器内、Kubernetes。
---
  ### 3.3 gitlab Runner的安装
  -  (1)安装方式一：手动下载rpm包
      ```js
        // 第一步：清华镜像安装16.11.0，适配上面的16.11.0版本的gitlab
        wget "https://mirrors.tuna.tsinghua.edu.cn/gitlab-runner/yum/el9-x86_64/Packages/g/gitlab-runner-16.11.0-1.x86_64.rpm"    -O gitlab-runner-16.11.0.rpm
        // 第二步：本地下载gitlab runner
        sudo dnf localinstall -y gitlab-runner-16.11.0.rpm
        // 第三步：启动runner
        sudo systemctl start gitlab-runner
        # 开机自启
        sudo systemctl enable gitlab-runner
        # 检查状态
        sudo systemctl status gitlab-runner
      ```
  - (2)安装方式三：通过docker安装
      ```js
        // 第一步：创建目录/data/devops/gitlab
        // 第二步：在devops文件夹下创建gitlab-runner文件夹
        // 第三步：gitlab文件夹下创建config文件夹
        // 第四步：cd至根目录
        // 第五步：
        docker run -itd -v /data/devops/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner:v18.9.0
      ```
---
  ### 3.4 gitlab Runner的分类及注册
  |        类型         | 作用范围 |    谁可以用      |
  |:-------------------:|:--------:|:----------------:|
  | **Instance Runner** | 整个平台 | 整GitLab所有项目 |
  |   **Group Runner**  | 指定群组 |   群组内所有项目 |
  |  **Project Runner** | 单个项目 |      仅该项目    |
---
  ### 3.5 gitlab Runner的状态
  - (1)locked：锁定状态，无法运行项目作业。
  - (2)paused:暂停状态，不会运行作业。
---
  ### 3.6 gitlab runner的注册
  > gitlab runner的注册分为三步：  
  > 第一步：获取注册令牌，不同类型的gitlab runner的令牌获取方式不同。  
  > 第二步：执行注册并选择执行器：执行方式分为交互式注册过程和非交互式两种,非交互式通过gitlab界面注册。  
  > 第三步：对上个步骤选择的不同执行器进行注册：gitlab runner有多种执行器：比如shell执行器，docker执行器。
  - 第一步：获取注册令牌
  ```
  (1)**实例级 Runner**:
    Admin Area → CI/CD → Runners → 找到 Registration token 并复制
  (2)**群组级 Runner**:
    群组 → Settings → CI/CD → Runners → Expand → 找到 Registration token 并复制
  (3)**项目级 Runner**:
   群组 → Settings → CI/CD → Runners → Expand → 找到 Registration token 并复制
  ```
  - 第二步：执行注册并选择执行器
  ```js
  // 交互式注册：
  - sudo gitlab-runner register
  - Enter the GitLab instance URL:http://192.168.1.100
  - Enter the registration token:刚才复制的令牌
  - Enter a description for this runner:my-app
  - Enter tags for the runner (comma-separated):build,deploy,linux，标签用于 .gitlab-ci.yml 中指定 runner
  - Enter an executor:可选：shell, docker, docker+machine, kubernetes, custom, ssh, parallels, virtualbox
  // 非交互式：
  ```
  - 第三步：不同执行器的注册
  ```js
  // shell执行器
  sudo gitlab-runner register \
  --non-interactive \
  --url "http://192.168.1.100" \
  --token "你的注册令牌" \
  --executor "shell" \
  --description "Shell Runner"
  // Docker 执行器:
  // 先安装 Docker
  sudo dnf install -y docker-ce docker-ce-cli containerd.io
  sudo systemctl start docker
  sudo systemctl enable docker

  // 再注册 Docker 执行器
  sudo gitlab-runner register \
    --non-interactive \
    --url "http://192.168.1.100" \
    --token "你的注册令牌" \
    --executor "docker" \
    --docker-image "alpine:latest" \
    --description "Docker Runner"
  ```
---
  ### 3.7 验证注册成功
  ```
    # 查看已注册的 Runner
    sudo gitlab-runner list
    # 输出示例：
    # Runtime          Executor
    # Shell Runner     shell
  ```
  ### 3.8 执行器分类：Shell, Docker, Kubernetes
---

## 四、pipeline语法
  ```
    +--------Pipeline---------------------------------------------+
    |                                                             |
    |    +--------------------build-jobs---------------------+    |
    |    |  +-----------+  +------------+  +------------+    |    |
    |    |  | Stage 1   |->| Stage 2    |->| Stage 3    |    |    |
    |    |  +-----------+  +------------+  +------------+    |    |
    |    +---------------------------------------------------+    |
    |                                                             |
    |                                                             |
    |    +-------------------deploy-jobs---------------------+    |
    |    |  +-----------+  +------------+  +------------+    |    |
    |    |  | Stage 1   |->| Stage 2    |->| Stage 3    |    |    |
    |    |  +-----------+  +------------+  +------------+    |    |
    |    +---------------------------------------------------+    |
    +-------------------------------------------------------------+
  ```
  ### 4.1 pipeline
  > 一次pipeline相当于一次构建任务，里面可以包含多个流程，如安装依赖，运行测试，编译，部署测试服务器，部署生产服务器等流程。
---
  ### 4.2 job
  > jobs表示构建工作，表示在某个stage中执行的工作。如果多个jobs之间的stage是相同的，那么这些job会是并行执行的，只有当所有的jobs都成功时该stage才会成功。
---
  ### 4.3 stages和stage
  > 一次pipeline中可以包含多个stages,所有的stages会**按照顺序执行**，只有当所有的stages都完成时该构建任务才会成功。  
  > 同一阶段的作业并行运行，不同阶段按顺序执行。
  > stage是按照job定义的，它依赖于pipeline全局定义的stages。**不同job的同一个stage可以并行执行,前提是需要对应的runner的作业数量改成不是1。详细修改方法如下：vim /etc/gitlab-runner/config.toml,然后修改concurrent = 2**。
---
  ### 4.4 script,before_script,after_script
  > 每个job作业中至少包含一个script。  
  > before_script:**它的运行失败会导致整个job失败，但不会导致after_script失败**。  
  > after_script:用于定义将在每个作业之后运行的命令。**job的失败不会导致after_script失败**。
  ```
    before_script:
      - echo "所有jobs运行之前"
    
    stages:
      - build
      - deploy
    
    build-jobs:
      stage: build
      tages:
        - share
      script:
        - echo "正在build项目"
        - echo "npm install"
        - echo "npm run build"
      before_script:
        - echo "build之前运行的脚本"
      after_script:
        - echo "build之后运行的脚本"
      allow_failure: true
    
    deploy-jobs:
      when: manual
      stage: deploy
      tags:
        - group
      script:
        - echo "正在部署中..."

    after_script:
      - echo "所有jobs运行之后"
  ```
---
  ### 4.5 .pre和.post
  > .pre始终是**整个pipeline**的**第一个运行阶段**，.post是**最后一个运行阶段**。  
  > 如果整个pipeline仅包含.pre和.post阶段的作业,则不会创建管道。
  ```
  .pre stage -->  build stage --> deploy stage --> .post stage
  ```
---
  ### 4.6 variables
  > 定义变量，包括job变量，pipeline变量，runner变量三种，其中优先级顺序为job＞pipeline＞runner。  
  > runner变量不会被job和pipeline变量覆盖
  - runner变量
  - pipeline变量
  - job变量
  - 预定义变量
    - CI_DEFAULT_BRACH:项目默认分支的名称
    - CI_COMMIT_BRANCH:提交分支名称
    - CI_COMMIT_DESCRIPTION:提交的描述
---
  ### 4.7 tags
  > 用于从允许运行该项目的所有runner列表中选择特定的runner，在runner注册期间，您可以指定runner的标签
---
  ### 4.8 allow_failure
  > **允许job失败**，默认值为**false**，启用之后，如果job失败，该job将在用户界面中显示橙色警告，但是**管道默认该job是成功的，并且pipeline不会被阻塞**
---
  ### 4.9 when
  > 用于实现在发生故障时运行或尽管发生故障也运行的作业
  ```
  - (1)on_success:前面的stages中的所有job都成功时才执行该job，默认值
  - (2)on_failure:当前面stages出现任意一个job失败时执行
  - (3)always：总是执行该作job
  - (4)manual:手动执行job
  - (5)delayed：延迟执行job
  // 举例
  deploy:
    when: manual
    script:
      - echo "deploy"
  ```
---
  ### 4.8 retry
  > 配置当作业失败时重新尝试的次数。  
  > max:最大重试次数为2次，最多一共运行3次！！  
> when：重试失败的错误类型。默认在失败情况下重试作业。  
  ```js
  // when的类型如下：
  // (1)always:在发生任何故障时重试
  // (2)unknow_failure:当前面阶段出现失败时执行
  // (3)script_failure：脚本失败时重试
  // (4)api_failure:API失败重试
  retry:
    max:2
    when:
    - script_failure
  ```
---
  ### 4.9 timeout
  > 超时包括三种，作业超时，项目超时，runner超时。  
  > 作业级别的超时可以超过项目超时，但是不能超过runner超时。
  ```
  // (1)instance runner超时 大于项目超时
  instance runner的超时为24h,项目为2h时，2h后该工作超时
  // (2)无instance runner超时，但是有项目超时
  无instance runner超时，项目超时时间为2h时，2h后该工作超时
  // (3)instance runner超时 小于项目超时
  instance runner的超时为2h,项目为24h时，2h后该工作超时
  build:
    script:
      - echo "deploy"
    timeout: 1h 30m
  ```
---
  ### 4.10 parellel
  > 配置要并行运行的作业实例数，此值必须**>=2,<=50**。  
  >  这会导致pipeline中的某个job并行运行N次。
  ```js
    build:
      script:
        - echo "deploy"
      parellel: 5
  ```
---


---
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
  