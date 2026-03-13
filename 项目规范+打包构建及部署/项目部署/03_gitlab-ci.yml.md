# 一：名词解释：
  ### 0.pipeline
  一次pipeline相当于一次构建任务，里面可以包含多个流程，如安装依赖，运行测试，编译，部署测试服务器，部署生产服务器等流程。
  ```js
    +----------------+           +----------+
    | Commit / Merge +---------->+ Pipeline |
    +----------------+           +----------+
  ```
  ### 1.job
    - jobs表示构建工作，表示在某个stage中执行的工作。如果多个jobs之间的stage是相同的，那么这些job会是并行执行的，只有当所有的jobs都成功时该stage才会成功。
    ```js
      +---------------------------------------+
      |                                       |
      |  Pipeline                             |
      |                                       |
      | +---------------------+               |
      | | Job 1               |               |
      | |      +---------+    |               |
      | |      | Stage 1 |    |               |
      | |      +---------+    |               |
      | |                     |               |
      | +---------------------+               |
      |                                       |
      |                                       |
      | +---------------------+               |
      | | Job 2               |               |
      | |      +---------+    |               |
      | |      | Stage 1 |    |               |
      | |      +---------+    |               |
      | |                     |               |
      | +---------------------+               |
      +---------------------------------------+
    ```
  ### 2.script：
   - 每个job作业中至少包含一个script。
   - before_script:**它的运行失败会导致整个job失败，但不会导致after_script失败**。
   - after_script:用于定义将在每个作业之后运行的命令。**job的失败不会导致after_script失败**。
    ```js
      job名称:
        script:
          - uname -a
          - bundle exec rspec
    ```
  ### 3.stages
   - 一次pipeline中可以包含多个stages,所有的stages会**按照顺序执行**，只有当所有的stages都完成时该构建任务才会成功。
   - 同一阶段的作业并行运行，不同阶段按顺序执行
    ```js
      +--------------------------------------------------------+
      | Pipeline                                               |
      |                                                        |
      | +-----------+  +------------+  +------------+          |
      | | Stage 1   |->| Stage 2    |->| Stage 3    |          |
      | +-----------+  +------------+  +------------+          |
      +--------------------------------------------------------+
    ```
    ```js
      stages:
        - build
        - test
        - codescan
        - deploy
    ```
  ### 4..pre和.post
    ```js
      codescan:
        stage: .pre
        script:
        - echo 'codescan'
    ```
  ### 5.tags
    用于从允许运行该项目的所有runner列表中选择特定的runner，在runner注册期间，您可以指定runner的标签
      ```js
        windows job:
        stage:
          - build
        tags:
          - windows
        script:
          - echo Hello
      ```
  ### 6.allow_failure
    **允许作业失败**，默认值为**false**，启用之后，如果作业失败，该作业将在用户界面中显示橙色警告，但是**管道默认该作业是成功的，并且pipeline不会被阻塞**
      ```js
        windows job:
        stage:
          - build
        tags:
          - windows
        script:
          - echo Hello
        allow_failure: true
      ```
  ### 7.when：控制作业运行
   - (1)on_success:前面的阶段中的所有作业都成功时才执行作业，默认值
   - (2)on_failure:当前面阶段出现失败时执行
   - (3)always：总是执行该作业
   - (4)manual:手动执行作业
   - (5)delayed：延迟执行作业
    ```js
      deploy:
        when: manual
        script:
          - echo "deploy"
    ```
  ### 8.retry：精准失败重试
  - 配置当作业失败时重新尝试的次数。
  - max:最大重试次数为2次，最多一共运行3次！！
  - when：重试失败的错误类型。默认在失败情况下重试作业
    ```js
      // when的类型如下：
      // (1)always:在发生任何故障时重试
      // (2)unknow_failure:当前面阶段出现失败时执行
      // (3)script_failure：脚本失败时重试
      // (4)api_failure:API失败重试
      // ...更多
      retry:
        max:2
        when:
        - script_failure
    ```
  ### 9.timeout：
   - 超时包括三种，作业超时，项目超时，runner超时
   - 作业级别的超时可以超过项目超时，但是不能超过runner超时
    ```js
      build:
        script:
          - echo "deploy"
        timeout: 1h 30m
    ```
  ### 10.parellel:并行作业
   - 配置要并行运行的作业实例数，此值必须**>=2,<=50**,这会导致pipeline中的某个job并行运行N次。
    ```js
      build:
        script:
          - echo "deploy"
        parellel: 5
    ```
  ### 11.only，except
   - only和except正在逐渐被rules替换，**only用来定义哪些分支和标签的git项目将被job执行**
   - except定义那些分支和标签的git项目将不会被执行。

  ### 12.rules
    - rules允许按照顺序评估单个规则，直到匹配并为作业动态提供属性，rules不能与only、except组合使用 ，rules可用的规则包括if,changes,exists
    - if：条件匹配
    - changes:文件变化
    - exists：检查文件是否存在
    ```js
      variables:
        DOMAIN: example.com
      rules: 
        - if:'$DOMAIN' == "example.com"
          when:manual
        - when:on_success
      // ========
      rules: 
        - changes:
          - Dockerfile
          when:manual
      // ========
      rules: 
        - exists:
          - Jenkinsfile
          when:manual
    ```
  ### 13.workflow
    - 顶级的workflow关键字适用于整个管道，并将确定是否创建管道
    - when:可以设置为always或者never，如果未提供，则默认值为always
    ```js
      variables:
        DOMAIN: example.com

      workflow:
        rules:
          - if:'$DOMAIN' == "example.com"
          when:always
        - when:never
    ```
  ### 14.cache
    - 存储编译项目所需的运行时的依赖项，指定项目工作空间中需要在job之间缓存的文件或目录。
    - 全局cache定义在job之外，针对所有job生效，job中cache优先于全局。
    - 当多个job之间需要共享缓存的时候，就需要传递
    - key:缓存标记，为不同的job定义不同的key时，会为每个job分配一个独立的cache
    - key:flies:文件变化时自动创建缓存
    - prefix：prefix:允许给定prefix的值与指定
    - policy:缓存策略，默认在执行开始时下载文件，并在结束时重新上传文件，policy：pull跳过下载步骤，policy：push跳过上传步骤
    ```js
      // 缓存流程
      // job1下载缓存文件--> script --> job1上传缓存文件 --> job2下载缓存文件--> script --> job2上传缓存文件
      // 会缓存target目录下的所有.jar文件
      build
        script:test
        cache:
          key: 
            files:
              - package.json
          paths:
            - target/*.jar
    ```
  ### 15.artifacts:制品
    - 用于指定在多页成功或者失败时应附加到作业的文件或者目录列表
    - name:制品名称
    - expose_as用于在合并请求中公开作业工件
    - when:制品创建条件，用于在作业成功或者失败时创建
    - expire_in:制品保留时间
    - report:junit:单元测试报告
      ```js
        job:
          artifacts:
           expire_in: 1 week
      ```
  ### 16.dependencies:获取制品
  ### 17.needs
    - 可无序执行作业，无需按照阶段顺序运行某些作业，可以让多个阶段同时运行
    - artifacts:用来控制工件下载，默认为false
      ```js
        module-a-test
          stage:test
          script:
            - echo "hello"
          needs:
            - job: 'module-a-build'
      ```
  ### 18.include
    - local:引入本地配置：可以允许引入外部YAML文件,文件具有扩展名.yml或者.yaml，使用合并功能可以自定义和覆盖包含本地定义的CICD配置，引入同一存储库中的文件使用相对于根目录的完整路径进行引用，与配置文件在同一分支上使用
    - file:
    - template:官方配置
    -remote:引入远程配置
    ```js
      include：
        local:'ci/localci/yml'
    ```
    ```js
      include:
        - project: 'cidevops/cidevops-gitlabci-service'
          ref: master
          file: 'jobs/build.yml'
      variables:
        BUILD_SHELL: 'npm run build'
        CACHE_DIR: 'dist/'
      cache:
        paths:
          - ${CACHE_DIR}
          - node_moduules/
      stages:
        - install
        - build
      install:
        stage: install
        script:
          - 'npm install'
      build:
        stage: build
        extends: .build
    ```
  ### 19.extends
    ```js
      .test:
        script:
        stage: test
      testjob:
        extends: .tests
    ```
  ### 20.trigger
    - 当gitlab从trigger定义创建的作业启动的时候，将创建一个下游管道
    - 多项目管道和子管道
    - 将trigger和when:manual一起使用会导致错误
    - **多项目管道**：跨多个项目设置流水线，以便一个项目中的管道可以触发另一个项目中的管道
    - **父子管道**：在同一个项目中管道可以触发一组同时运行的子管道，子管道仍然按照阶段顺序执行器每个作业，但是可以自由地继续执行作业阶段，无需等待父管道中的作业。
    - 当前面的阶段运行完成后，触发某一个项目的master流水线，创建上游管道的用户需要具有对下游项目的访问权限，如果发现下游项目用户没有访问权限，则staging作业将被标记为失败
    ```js
      staging:
        variables:
          ENVIROMENT: staging
        stage: deploy
        trigger:
          project: #用于指定下游项目的完整路径
          branch: master指定的项目分支名，使用variables关键字将变量传递到下游管道
          strategy: depend将自身状态从触发的管道合并到源网桥作业
    ```
  ### 21.image
    - 第一步：注册一个工作类型为docker的runner
      ```js
        gitlab-runner register \
          --non-interactive \
          --executor "docker" \
          --docker-image alpine:latest \
          --url "http://106.14.38.228/" \
          --registration-token "dwe1kTT9v8bZcqyBupB7" \
          --description "devops-runner" \
          --tag-list "build,deploy" \
          --run-untagged="true" \
          --locked="false" \
          --access-level="not_protected" 
      ```
    - images:默认在注册runner的时候需要填写一个基础的镜像，只要使用执行器为docker类型的runner，所有的操作运行都会在容器中运行。
    - 如果全局指定了image则所有作业使用此image创建容器并在其中运行。
    - 全局未指定image，再次查看job中是否有指定，如果有此job按照指定镜像创建容器并运行，没有则使用注册runner时的指定默认镜像。
  ### 22.services
    - 工作期间运行的另一个docker映像，并link到image关键字定义的docker映像，这样您就可以在构建期间访问服务映象。
      ```js
        before_script:
          - ls
        services:
          - name mysql:latest
          alias: mysql-1
      ```
  ### 23.environment
    ```js
      deploy:
        stage:deploy
        script: git push production HEAD:master
        environment:
          name: production
          url: https://prod.example.com
    ```
  ### 24.inherit
    - 使用或者禁用全局定义的环境变量或者默认值
    ```js
      // 使用方式一：true/false
      inherit:
        default: false
        variables: false
      // 使用方式二：继承部分变量或者默认值
      inherit:
        default:
          - 变量一
          - 变量二
        variables:
          - v1
          - v2
    ```
# 实例
  ```js
    // 构建阶段-任务,包含五个stage:analytics,test,build,package,deploy
    stages:
      - analytics
      - test
      - build
      - package
      - deploy

    // 构建工作job名称
    build_analytics:
      // 该工作执行阶段
      stage: analytics
      // 设置只对master分支有效
      only:
        - master
        - tags
      tags:
        - runner-tag-snoreqube
      script:
        - echo "=============== 开始代码质量检测 ==============="
        - echo "=============== 结束代码质量检测 ==============="

    build_test:
      stage: test
      only:
        - master
        - tags
      tags:
        - runner-tag
      script:
        - echo "=============== 开始测试任务 ==============="
        - echo "=============== 结束测试任务 ==============="


    build:
      stage: build
      only:
        - master
        - tags
      tags:
        - runner-tag
      script:
        - echo "=============== 开始编译任务 ==============="
        - echo "=============== 结束编译任务 ==============="

    package:
      stage: package
      tags:
        - runner-tag
      script:
        - echo "=============== 开始打包任务 ==============="
        - echo "=============== 结束打包任务 ==============="

    deploy_test:
      stage: deploy
      tags:
        - runner-tag
      // 输出在gitlab-ci中设置的变量
      script:
        - echo "=============== 自动部署到测试服务器 ==============="
        - echo "测试服务器:" ${SERVER_TEST}
      #环境变量
      environment:
        name: test
        url: https://staging.example.com

    deploy_test_manual:
      stage: deploy
      tags:
        - runner-tag
      script:
        - echo "=============== 手动部署到测试服务器 ==============="
      environment:
        name: test
        url: https://staging.example.com
      // 设置条件 manual 允许失败  
      when: manual

    deploy_production_manual:
      stage: deploy
      tags:
        - runner-tag
      script:
        - echo "=============== 手动部署到生产服务器 ==============="
        - echo "测试服务器:" ${SERVER_TEST}
      environment:
        name: production
        url: https://staging.example.com
      when: manual
  ```