# 一：名词解释：


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