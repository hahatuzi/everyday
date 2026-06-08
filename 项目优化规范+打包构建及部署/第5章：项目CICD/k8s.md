# 容器化部署分析：
  ## 优点：
  - 每个容器都拥有自己的文件系统，CPU,内存
  - 容器化的应用程序可以跨云服务商，操作系统部署
  ## 缺点：
  - 一个容器如果鼓掌，如何才能让另外一个容器立刻启动去替补停机的容器
  - 并发访问量变大的时候，如何才能做到横向扩展容器数量，以上问题统称为容器编排问题
# k8s
  ## 1.概念：
  K8s本质是一组服务器集群。一个k8s集群主要由**控制节点master**,**工作节点node**构成。目的是实现资源管理的自动化，主要提供以下功能：
  - 自我修复:一旦某个容器崩溃，能够在1s左右启动新的容器
  - 弹性伸缩：可以对正在运行的容器数量进行调整
  - 服务发现：通过自动发现的形式找到它依赖的服务
  - 负载均衡：如果一个服务启动了多个容器，能够自动实现请求的负载均衡
  - 版本回退：如果新版本有问题，可以立即回退
  - 存储编排：可以根据容器自身的需求自动创建存储卷
  ## 2.master：集群控制节点，灭一个k8s都至少要有一个master节点，集群的控制平面，负责集群的决策：
  - Apiserver:资源操作的唯一入口，接收用户输入的命令，提供认证，授权，API注册和发现等机制
  - Scheduler:负责调度集群资源
  - ControllerManager：负责维护集群的状态，比如程序的更新，销毁等
  - Etcd:负责村出纳集群中各种资源的信息
  ## 3.node:工作负载节点，集群的数据平面，负责为容器提供运行环境（干活）
  - Kubelet：负责维护容器的生命周期，即通过docker，来创建，更新，销毁容器
  - KubeProxy：负责提供集群内部的服务发现和负载均衡
  - Docker：负责节点上容器的各种操作
  ## 4.nginx服务调用实例：
  - 第一步：k8s启动，mster,node将自己的信息存储在etcd数据库中
  - 第二步：nginx安装服务请求会被发送到master节点的apiServer组件
  - 第三步：apiServer组件调用scheduler组件，决定nginx服务安装到哪个node节点上
  - 第四步：apiServer调用controller-manager去调度Node节点，来安装nginx服务
  - 第五步：kubelet接到指令后，会通知docker，然后由docker来启动一个nginx的pod,pod是k8s的最小操作单元，容器必须跑在pod中
  - 第六步：nginx服务运行成功，如果需要访问nginx，需要通过kube-proxy来对pod产生访问代理，这样就可以访问集群中的nginx服务
  ## 5.Pod:k8s的最小控制单元，容器都是运行在pod中的，一个pod中可以有1个或者多个容器
  ## 6.Controller:控制器，通过它来实现pod的管理，比如启动，停止pod，伸缩pod的数量等
  ## 7.Service:pod对外服务的统一入口
  ## 8.Label:标签，用于对pod进行分类，同一类pod会拥有相同的标签
  ## 9.NameSpace:命名空间，用来隔离pod的运行环境
# 三：集群环境搭建
  ## 1.集群类型：
  - 一主多从:
  - 多主多从：多台master多台Node
  ## 2.搭建步骤：
  - 集群所需组件安装
  - 集群安装
    ```js
      kubectl get nodes
    ```
  - 网络插件安装
  - 环境测试
# 资源管理
  ## 1.资源管理方式：
  ### (1)命令式对象管理：直接使用命令去操作kubernetes资源
  > kubectl run nginx-pod --image=nginx:1.17.1 --port=80
  ### (2)命令式对象配置：通过命令配置和配置文件去操作kubernetes资源
  > kubectl create/patch -f nginx-pod.yaml
  ### (3)声明式对象配置：通过apply命令和配置文件去操作kubernetes资源
  > 使用apply操作资源：如果资源不存在就创建，相当于kubectl create,存在就更新相当于kubectl patch
  > kubectl apply -f nginx-pod.
  ---
  > 使用推荐
  > 创建、更新资源：使用kubectl apply -f xxx.yaml
  > 删除资源：使用kubectl delete xxx.yaml
  > 查询资源：使用kubectl get 资源名称
  ### 使用推荐
  ## 2.kubectl命令
  > kubectl [command] [type] [name] [flags]
  - command:指定要对资源执行的操作,比如create,get,delete
  - type:指定资源类型，比如deployment,podd,service
  - name:指定资源的名称，名称大小写敏感
  - flags:指定额外的可选参数
  ## 实例
  - kubectl create ns dev
  - kubectl get ns
  - kubectl run pod --image=nginx:1,17,1 -n dev

# 重要概念
  ## nameSpace
  Namespace是kubernetes系统中一种非常重要的资源，它的主要作用是实现**多套环境的资源隔离或者多租户的资源隔离**。比如将两个pod划分到不同的Namespace中
  - kubectl get namespace
  - kubectl create -f ns-dev.yaml
  - kubectl delete -f ns-dev.yaml
    ### 1.kubernetes在集群启动后会默认创建几个namespace
    - default:所有未指定Namespace的对象都会被分配在default命名空间
    - kube-node-lease：集群节点之间的心跳维护
    - kube-public：次命名空间中的资源可以被任何人访问
    - kube-system：所有由kubernetes系统创建的资源都处于这个命名空间
    ### 2.常见命令
    - kubectl get ns:查看所有的命名空间
  ## pod
  pod是Kubernetes集群管理的最小单元，程序要运行必须部署在容器中，二容器必须存在于pod中
  - 