# pipeline
一次pipeline相当于一次构建任务，里面可以包含多个流程，如安装依赖，运行测试，编译，部署测试服务器，部署生产服务器等流程。
```js
+----------------+           +----------+
|                |  trigger  |          |  
| Commit / Merge +---------->+ Pipeline |
|                |           |          |
+----------------+           +----------+
```
# stages
一次pipeline中可以包含多个stages,所有的stages会按照顺序执行，只有当所有的stages都完成时该构建任务才会成功
```js
+--------------------------------------------------------+
|                                                        |
| Pipeline                                               |
|                                                        |
| +-----------+  +------------+  +------------+          |
| | Stage 1   |->| Stage 2    |->| Stage 3    |          |
| +-----------+  +------------+  +------------+          |
|                                                        |
+--------------------------------------------------------+
```
# jobs
jobs表示构建工作，表示在某个stage中执行的工作。如果多个jobs之间的stage是相同的，那么这些job会是并行执行的，只有当所有的jobs都成功时该stage才会成功。
```js
+---------------------------------------+
|                                       |
|   Stage 1                             |
|                                       |
|        +---------+                    |
|   -->  | Job 1   |                    |
|        +---------+                    |
|        +---------+                    |
|   -->  | Job 1   |                    |
|        +---------+                    |
|        +---------+                    |
|   -->  | Job 1   |                    |
|        +---------+                    |
+---------------------------------------+
// 或者用以下方式进行理解
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
# script
每个job作业中至少包含一个script
# before_script
分为全局和job内，job内的before_script会替换全局before_script
# after_script:用于定义将在每个作业之后运行的命令
```js
stages:
  - analytice
  - test
  - build
  - deploy
analytice_step:
  stage: analytice
  script:
    - echo "analytice"
```
比如以下示例
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
```js
.build:
  stage: build
  tags:
    - build
  script:
    - $BUILD_SHELL
    - ls
```
# 前端pipeline中需要的操作
<1>install阶段：
就是执行npm install 命令，根据package.json安装node_modules依赖包
<2>eslint阶段
执行eslint检查，判断代码格式是否符合规范，如果不符合停止pipeline
<3>build阶段
编译成生产代码，可以通过webpack之类的打包工具执行编译，也可以通过脚手架自身提供的编译命令进行编译,如npm run build
<4>deploy阶段
部署阶段，将刚才的build阶端生成的生产代码部署到生产访问的服务器上，
```js
stages: # 分段
  - install
  - eslint
  - build
  - deploy
 
cache: # 缓存
  paths:
    - node_modules
    - build
 
install-job:
  tags:
    - sss
  stage: install
  script:
    - npm install
 
eslint-job:
  tags:
    - sss
  stage: eslint
  script:
    - npm run eslint
 
build-job:
  tags:
    - sss
  stage: build
  script:
    - npm run build
 
deploy-job:
  tags:
    - sss
  stage: deploy
  script:
    - sshpass -p $PASSWORD scp -r ./build $CUSTOM_USERNAME@$CUSTOM_IP:/var/www/html
```