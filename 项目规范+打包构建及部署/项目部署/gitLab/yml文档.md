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
# tags
用于从允许运行该项目的所有runner列表中选择特定的runner，在runner注册期间，您可以指定runner的标签
# allow_failure
允许作业失败，默认值为false，启用之后，如果作业失败，该作业将在用户界面中显示橙色警告，但是**管道默认该作业是成功的，并且pipeline不会被阻塞**
# when，控制作业运行
 (1) on_success:前面的阶段中的所有作业都成功时才执行作业，默认值
（2）on_failure:当前面阶段出现失败时执行
（3）always：总是执行作业
  (4)manual:手动执行作业
  (5)delayed：延迟执行作业
```js
deploy:
  when: manual
  script:
    - echo "deploy"
```
#　retry
配置当作业失败时重新尝试的次数。max:最大重试次数 when：重试失败的错误类型
when的类型包括：always(在发生任何故障时重试)，unknow_failure,script_failure
```js
retry:
  max:1
  when:
   - script_failure
```
# timeout：超时包括三种，作业超时，项目超时，runner超时
作业级别的超时可以超过项目级别的超时，但是不能超过runner级别的超时时间，
# parellel
配置要并行运行的作业实例数，此值必须>=2,<=50,这会导致pipeline中的某个job并行运行N次。
# only，except
only和except正在逐渐被rules替换，only用来定义哪些分支和标签的git项目将被job执行
except定义那些分支和标签的igt项目将不会被执行。
# rules
rules不能与
# workflow
# cache
cache:
  key:
    files:
      - package.json #当该文件发生变化时创建缓存
    paths:
      
# needs
可无序执行作业，无需按照阶段顺序运行某些作业，可以让多个阶段同时运行
# include
local:引入本地配置：可以允许引入外部YAML文件,文件具有扩展名.yml或者.yaml
使用合并功能可以自定义和覆盖包含本地定义的CICD配置
引入同一存储库中的文件使用相对于根目录的完整路径进行引用，与配置文件在同一分支上使用
include：
  local:'ci/localci/yml'
# extends
# trigger
### 多项目管道：跨多个项目设置流水线，以便一个项目中的管道可以触发另一个项目中的管道
### 父子管道，在同一个项目中管道可以触发一组同时运行的子管道，子管道仍然按照阶段顺序执行器每个作业，但是可以自由地继续执行作业阶段，无需等待父管道中的作业。
多项目管道：当前面的阶段运行完成后，触发某一个项目的master流水线，创建上游管道的用户需要具有对下游项目的访问权限，如果发现下游项目用户没有访问权限，则staging作业将被标记为失败
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
# image
images:默认在注册runner的时候需要填写一个基础的镜像，只要使用执行器为docker类型的runner，所有的操作运行都会在容器中运行，如果全局指定了image则所有作业使用此image创建容器并在其中运行，全局未指定image，再次查看job中是否有指定，如果有此job按照指定镜像创建容器并运行，没有则使用注册runner时的指定默认镜像
# services
工作期间运行的另一个docker映像，并link到image关键字定义的docker映像，这样您就可以在构建期间访问服务映象。
# environment
```js
deploy to production
  stage:deploy
  script: git push production HEAD:master
  environment:
    name: production
    url: https://prod.example.com
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