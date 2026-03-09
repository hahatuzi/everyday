

# 二：Gitlab Runner

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