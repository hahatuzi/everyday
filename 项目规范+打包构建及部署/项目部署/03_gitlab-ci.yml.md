# 一：名词解释：
  ### 1.job
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
  ### 19.extends
    ```js
      .test:
        script:
        stage: test
      testjob:
        extends: .tests
    ```
1.文件解读
```js
  stages:
    - build
    - test
    - codescan
    - deploy
```