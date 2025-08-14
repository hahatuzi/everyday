# 一.传统项目的部署
  - 1.静态资源上传服务器，nginx代理
  - 2.CI平台，jenkins,gitlab代码通过ci代码源拉到构建机器，进行打包部署
  - 3.云效，github action, circleCI云平台。
  ### 部署的触发方式：push触发部署，pr触发，打tag触发

# 二：CICD
  ### 1.概念：
  - 1.持续集成CI：频繁地将代码集成到主干,持续集成包括一个自动构建的过程(构建脚本和工具)，一个代码存储库(版本管理系统)，一个持续集成服务器（如jenkins）.
  - 2.持续交付：频繁地将软件的新版本交付给测试部门或者产品评审，如果通过就进入生产阶段。
  - 3.持续部署：持续部署是持续交付的下一步，指的是将代码自动部署到生产环境。实现任何时间都可以部署代码进入生产阶段。
  ### 2.工作流程
    - 第一步：代码提交至仓库,代码中配置push策略
    - 第二步：CI，缺陷扫描，ESLint检查，unit Test,自动触发构建脚本npm build
    - 第三步：CD,构建产物部署到环境：**ECS部署**或者**Docker**
  ### 3.工具链
    - 持续集成的工具：jenkins,github action,travis CI,circleCI
    - 持续交付：ArgoCD,spinnaker
    - 产物部署管理：docker compose,k8s

  ### 4.持续集成的优点：
     - 1.降低风险，由于持续集成不断去构建，编译，测试，可以很早的发现问题，所以修复的代价就很少
     - 2.对系统健康持续检查，减少发布风险带来的问题
     - 3.减少重复性工作
     - 4.持续部署，提供可不是单元包
     - 5.持续交付可供使用的版本


# 三：Docker
  ### docker的优势
  - 环境一致性
  - 高效利用，方便快捷使用轻量化容器
  - 服务于微服务架构
  ### 核心概念
  - 镜像
  - 容器
  - 仓库
  ### docker命令
  - docker ps:查看当前docker在跑哪些容器进程
  - docker container ls
  - docker container ls -a:查看所有的容器
  - docker images查看镜像
  ### dockerfile文件解读
    ```js
      FROM XXX // 选择镜像
      WORKDIR
      COPY
      RUN npm install
      EXPOSE 3000
      CMD ['npm', 'start']

      // docker build -t XXX
      // docker run -d --name XXX
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
