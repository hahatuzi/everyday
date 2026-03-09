# 一：gitlab CICD
  ### 1.组成
  - gitlab CI/CD
  - gitlab runner:是一个单独处理构建的应用程序，它可以单独部署，并通过API与gitlab CI/CD一起使用。**gitlab-runner可以在不同的主机上部署，也可以在同一个主机上设置多个gitlab-runner ,还可以根据不同的环境设置不同的环境，比如我们需要区分研发环境，测试环境以及正式环境等。**
  - gitlab-ci.yaml
  ### 2.工作流程
  push code --> trigger a pipeline --> gitlab-ci.yml --> gitlab CI pipelineCI pipeline(preparation -- build -- tests) --> Deploy对应多个gitlab runner(gitlab runner 可以是服务器或者docker容器)
  - 1.代码托管到git仓库
  - 2.项目根目录创建ci文件,gitlab-ci.yml,在文件中指定构建，测试和部署脚本
  - 3.gitlab检测到gitlab-ci.yml并使用gitlab runner 的工具运行脚本
  - 4.根据预定义的gitlab-ci.yml脚本分组成作业，并共同组成管道
  ### 3.gitlab CI/CD的特点
  - 1.多平台
  - 2.多语言
  - 3.稳定构建：构建与gitlab在不同的机器上运行
  - 4.并行构建：gitlab CI/CD在多态机器上拆分构建，从而实现快速执行
  - 5.实时日志记录
  - 6.灵活的管道
  - 7.版本管道：一个gitlab-ci.yml文件包含测试，整个过程的步骤

# 二：gitlab安装及使用
  ### 1.安装方式一：使用rpm包安装
    ```js
      // 第一步：下载gitlab镜像
      yum install curl policycoreutils-python openssh-server postfix wget -y
      wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
      // 第二步：安装gitlab
      rpm -ivh gitlab-ce-13.1.2-ce.0.el7.x86_64.rpm
      // 第三步：编辑站点地址
      vim /etc/gitlab.rb
      // 第四步：配置
      gitlab-ctl reconfigure
    ```
  ### 2.安装方式二：使用docker安装
  ```js
  mkdir -p ~/data/gitlub/config ~/data/gitlab/logs ~/data/gitlab/data
  docker pull gitlab/gitlab-ce:12.9.0-ce.0
  ```
  ### 3.gitlab常见命令
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
# 三：gitlab runner的安装与使用
[!参考文章-本机虚拟机安装gitlab]https://blog.csdn.net/qq_42141141/article/details/126397059