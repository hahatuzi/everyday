# 一.传统项目的部署
  - 1.静态资源上传服务器，nginx代理
  - 2.CI平台，jenkins,gitlab代码通过ci代码源拉到构建机器，进行打包部署
  - 3.云效，github action, circleCI云平台。
  ### 部署的触发方式：push触发部署，pr触发，打tag触发

# 二：CICD
  ### 1.概念：
  - 1.持续集成CI：每次代码提交都触发自动构建和测试。
  - 2.持续部署CD：持续部署是持续交付的下一步，指的是将代码自动部署到生产环境。
  ### 2.工作流程
    - 第一步：代码提交至仓库,代码中配置push策略
    - 第二步：CI，缺陷扫描，ESLint检查，unit Test,自动触发构建脚本,npm i && npm build
    - 第三步：CD,构建产物部署到环境：部署方式**ECS部署**或者**Docker**
  ### 3.工具链
    - 持续集成的工具：**jenkins**,**github action**,travis CI,circleCI，gitlab-CI
    - 持续交付：ArgoCD,spinnaker
    - 产物部署管理：**docker compose**, **k8s**

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
  - docker run --name miaoma-nginx-server -d -p 8080:80 nginx
  ### dockerfile文件解读
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

# 四：gitlab CICD
  ### 1.组成
  - gitlab CI/CD
  - gitlab runner:是一个单独处理构建的应用程序，它可以单独部署，并通过API与gitlab CI/CD一起使用
  - gitlab-ci.yaml
  ### 2.工作流程
  push code --> trigger a pipeline --> gitlab-ci.taml --> gitlab CI pipelineCI pipeline(preparation -- build -- tests) --> Deploy对应多个gitlab runner(gitlab runner 可以是服务器或者docker容器)
  - 1.代码托管到git仓库
  - 2.项目根目录创建ci文件,gitlab-ci.yml,在文件中指定构建，测试和部署脚本
  - 3.gitlab检测到它并使用gitlab runner 的工具运行脚本
  - 4.脚本被分组成作业，并共同组成管道
  ### 3.gitlab CI/CD的特点
  - 1.多平台
  - 2.多语言
  - 3.稳定构建：构建与gitlab在不同的机器上运行
  - 4.并行构建：gitlab CI/CD在多态机器上拆分构建，从而实现快速执行
  - 5.实时日志记录
  - 6.灵活的管道
  - 7.版本管道：一个gitlab-ci.yml文件包含测试，整个过程的步骤

# 五：Jenkins
  ### 1.jenkins三大概念：
  - 1.Job(任务):在jenkins平台中，都是以job任务的形式完成一件事情。
  - 2.plugins(插件)
  - 3.workspace(工作空间):jenkins是通过本地文件的形式来存储和管理数据的。jenkins下的每一个job都有属于自己的workspace,用来存放本任务涉及到的数据和文件

# 六：gitlab CICD和Jenkins对比
  ### 1.分支可配置性
  - （1）使用gitlab CI,新创建的分支无需任何进一步配置就可以立即使用CI管道中的已定义作业。
  - （2）jenkins基于gitlab的多分支流水线可以实现
  ### 2.定时执行构建任务
  - （1）jenkins可以在构建触发器中选择定时构建来实现某时刻的构建任务。
  - （2）但是gitlabCICD没有定时执行构建任务这一功能。不过可以通过webAPI使用同一台或者另一台服务器上的cronjob触发作业和管道。
  **尽管使用gitlab CI无法实现这一点，其实提交代码即触发流水线也没有什么不同，反而代码未提交时就构建反倒造成资源浪费**
  ### 3.拉取请求支持
  如果很好的集成了存储库管理器和CI/CD平台，您可以看到请求的当前构建状态，使用这种功能可以避免将带面合并到不起作用或者无法正确构建的主分支中。
  gitlab比起jenkins有天然的优势。
  ### 4.权限管理
  **从存储库管理器集成的权限管理对于不想为每个服务分别设置每个用户的权限的大型开发团队很有用，因为多数情况下两者的权限是一致的**
  - （1）gitlab可以实现存储库管理器和CI/CD平台之间的权限合并。
  - （2）jenkins并没有内置的存储库管理器，所以它无法直接在存储库管理器和CICD平台之间合并权限。
  ### 5.存储库交互
  - （1）gitlab CI是存储库管理器gitlab的固定组件。所以在CICD流程和存储库功能之间提供了良好的交互
  - （2）jenkins与存储库管理器之间是松散耦合的，所以选择版本控制系统时更加灵活。
  ### 6.插件管理
  - （1）gitlab是开放式的，任何人都可以直接向代码库做贡献
  - （2）jenkins是通过插件完成扩展功能的，但是插件的维护保护和升级成本很高