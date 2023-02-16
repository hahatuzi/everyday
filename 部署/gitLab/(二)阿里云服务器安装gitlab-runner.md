# 一：gitlabCICD优点:
    1.开源：CI/CD是开源gitlab社区版和转悠gitlab企业版额一部分
    2.易于学习：文档完善
    3.无缝集成：gitlabCICD是gitlab的一部分，支持从计划到部署，具有出色的用户体验
    4.可扩展：测试可以在单独的计算机上分布式与耐心你，可以根据需要甜腻骄傲任意数量的计算机
    5.更快的结果：每个构建可以拆分为多个作业。这些作业可以在多台计算机上并行运行
    6.针对交付进行了优化，多个阶段，手动部署，环境和变量
gitlabCICD的组件
1.gitlabcicd:GitLab CI是gitlab的开源持续集成服务，用于协调作业
2.gitlab runner:是一个处理构建的应用程序，可以单独部署，并通过api于gitlabcicd一起使用.gitlab Runner实际上都是docker container ,由gitlab Runner 来自动创建，运行的环境由gitlab Runner程序控制，使用docker来创建runner，使得每个虚拟环境都干净，轻量，相互隔离，互不影响.
**Runner就像一个个的工人，而Gitlab-CI就是这些工人的一个管理中心，所有工人都要在Gitlab-CI里面登记注册，并且表明自己是为哪个工程服务的。当相应的工程发生变化时，Gitlab-CI就会通知相应的工人执行软件集成脚本**

# 二：gitlab CICD实现流程
#### Gitlab Runner的实际执行情况
    (1)本地代码改动
    (2)变动代码推送到gitlab
    (3)gitlab将变更通知给gitlab-CI
    (4)gitlab-CI找到这个工程相关的gitlab-runner
    (5)gitlab-runner将代码更新到本地
    (6)根据预设值的条件配置好环境
    (7)根据预定义的脚本(,gitlab-ci.yml)执行
    (8)将执行结果通知给gitlab
    (9)gitlab显示最终执行的结果
**gitlab-runner可以在不同的主机上部署，也可以在同一个主机上设置多个gitlab-runner ,还可以根据不同的环境设置不同的环境，比如我们需要区分研发环境，测试环境以及正式环境等。**
#### Gitlab Runner的分类
    （1）shared:运行整个平台项目的作业(gitlab)
    （2）group:运行特定group下所有项目的作业(group)
    （3）specific：运行指定的项目作业（project）
#### gitlab Runner的状态
locked：无法运行项目作业，paused:不会运行作业
#### Gitlab Runner安装
支持运行在目前常用的平台上，例如：Linux/Unix、Windows、MacOS、Docker容器内、Kubernetes。
1.添加gitlab官方库
```js
 # For Debian/Ubuntu/Mint
 curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash

 # For RHEL/CentOS/Fedora
 curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
```
2.命令安装:
```js
// MacOS
sudo brew install gitlab-ci-multi-runner
// For Debian/Ubuntu/Mint

 sudo apt-get install gitlab-ci-multi-runner

 //For RHEL/CentOS/Fedora
 sudo yum install gitlab-ci-multi-runner

```
3.注册 gitlab-runner,查看gitlab的url和token
4.配置注册信息 gitlab-runner register
```js
Enter the GitLab instance URL (for example, https://gitlab.com/):
http://47.99.144.3/
Enter the registration token:
meAG8N_apx3bsBCCxRpL
Enter a description for the runner:
[iZq0jkhg8vdxw3Z]: my-app
Enter tags for the runner (comma-separated):
my-app
Enter optional maintenance note for the runner:

Registering runner... succeeded                     runner=meAG8N_a
Enter an executor: shell, virtualbox, docker-ssh+machine, instance, custom, docker, docker-ssh, parallels, kubernetes, ssh, docker+machine:
```
选择shell
#### gitlab常见命令
```js
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