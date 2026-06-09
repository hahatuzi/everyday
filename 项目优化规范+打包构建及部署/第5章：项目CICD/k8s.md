# k8s

---

## 目录

1. [容器化部署分析](#一容器化部署分析)
2. [k8s概念](#二k8s概念)
3. [master](#三master)
4. [node](#四node)
5. [NameSpace](#五NameSpace)
6. [Pod](#六Pod)
7. [Controller](#七Controller)
8. [Service](#八Service)
9. [Label](#九Label)

---

## 一、容器化部署分析
  ### 1.1 优点
  - 每个容器都拥有自己的文件系统，CPU,内存
  - 容器化的应用程序可以跨云服务商，操作系统部署
  ### 1.2 缺点
  - 一个容器如果鼓掌，如何才能让另外一个容器立刻启动去替补停机的容器
  - 并发访问量变大的时候，如何才能做到横向扩展容器数量，以上问题统称为容器编排问题
---

## 二、k8s概念
  >K8s本质是一组服务器集群。一个k8s集群主要由**控制节点master**,**工作节点node**构成。目的是实现资源管理的自动化，主要提供以下功能：
  - 自我修复:一旦某个容器崩溃，能够在1s左右启动新的容器
  - 弹性伸缩：可以对正在运行的容器数量进行调整
  - 服务发现：通过自动发现的形式找到它依赖的服务
  - 负载均衡：如果一个服务启动了多个容器，能够自动实现请求的负载均衡
  - 版本回退：如果新版本有问题，可以立即回退
  - 存储编排：可以根据容器自身的需求自动创建存储卷
---
## 三、master
  >集群控制节点，每一个k8s都至少要有一个master节点，集群的控制平面，负责集群的决策：
  - Apiserver:资源操作的唯一入口，接收用户输入的命令，提供认证，授权，API注册和发现等机制
  - Scheduler:负责调度集群资源
  - ControllerManager：负责维护集群的状态，比如程序的更新，销毁等
  - Etcd:负责村出纳集群中各种资源的信息
---
## 四、node
  >工作负载节点，集群的数据平面，负责为容器提供运行环境（干活）
  - Kubelet：负责维护容器的生命周期，即通过docker，来创建，更新，销毁容器
  - KubeProxy：负责提供集群内部的服务发现和负载均衡
  - Docker：负责节点上容器的各种操作
---
## 五、NameSpace
  >命名空间，用来隔离pod的运行环境,Namespace是kubernetes系统中一种非常重要的资源，它的主要作用是实现**多套环境的资源隔离或者多租户的资源隔离**。比如将两个pod划分到不同的Namespace中。
  ### 5.1 kubernetes在集群启动后会默认创建几个namespace
  - default:所有未指定Namespace的对象都会被分配在default命名空间
  - kube-node-lease：集群节点之间的心跳维护
  - kube-public：次命名空间中的资源可以被任何人访问
  - kube-system：所有由kubernetes系统创建的资源都处于这个命名空间
  ### 5.2 常见命令
  ```js
  kubectl get ns // 查看所有的命名空间
  kubectl get namespace
  kubectl create -f ns-dev.yaml
  kubectl delete -f ns-dev.yaml
  ```
---
## 六、Pod
  >pod是Kubernetes集群管理的最小单元，容器都是运行在pod中的，一个pod中可以有1个或者多个容器
  ### 6.1 pod配置
  - apiVersion:版本
  - kind:类型
  - metadata:元数据
  - spec:描述
  - spec-containers:容器列表
  - nodeName:根据nodeName的值将pod调度到指定的Node节点上
  - nodeSelector:根据NodeSelector中定义的信息将该Pod调度到包含这些label的Node上
  - hostNetWork:是否使用主机网络模式
  - volumes:存储卷，用来定义Pod上面挂载的存储信息
  - restartPolicy:重启策略
  - status:状态信息
  - name:容器名称
  - image:容器需要的镜像地址
  - imagePullPolicy:镜像拉取策略
  - command:容器的启动命令列表
  - args:容器启动命令需要的参数
  - env:容器环境变量的配置
  - ports:容器需要暴露的端口列表
  - resources:资源限制和资源请求的设置
  - limits:用于限制运行时容器的最大占用资源
  - requests:用于设置容器需要的最小资源
  ### 6.2 pod生命周期
  ```
  第一步： pod创建过程
    ──→ 用户通过kubectl或其他api客户端提交需要创建的pod信息给 apiServer
    ──→ apiServer开始生成pod对象的信息，并将信息存入etcd，然后返回确认信息至客户端
    ──→ apiServer开始反映etcd中的pod对象的变化，其它组件使用watch机制来跟踪检查apiServer上的变动
    ──→ scheduler发现有新的pod对象要创建，开始为Pod分配主机并将结果信息更新至apiserver
    ──→ node节点上的kubelet发现有pod调度过来，尝试调用docker启动容器，并将结果回送至apiServer
    ──→ apiServer将接收到的pod状态信息存入 etcd 中
  第二步： 运行初始化容器过程
    ──→ 容器必须按照顺序执行，前一个成功时后一个才能运行
  第三步： 运行主容器过程
  第四步： pod终止过程
    ──→ 用户想apiServer发送删除pod对象命令
    ──→ apiServer中的pod对象信息随时间推移更新，在默认宽限30s内pod被视为dead
    ──→ 将pod标记为terminating状态
    ──→ kubelet监控到pod状态更新为terminating时启动关闭pod
    ──→ 端点控制器监控到pod对象关闭时移除所有匹配到此端点的service资源的端点列表
    ──→ 如果当前pod对象定义了preStop钩子处理器，pod对象更新为terminating时同步执行preStop钩子处理器
    ──→ pod对象中的容器进程收到停止信号
    ──→ 宽限期结束后，若pod中还有仍在运行的进程，那么pod对象会收到立即终止的信号
    ──→ kubelet请求apiServer删除pod资源，宽限期设置为0，此时pod对用户已经不可见
  ```
  ### 6.3 pod的5种状态
  - 挂起：apiserver已经创建了pod资源对象，但尚未被调度完成，或者仍处于下载镜像的过程中
  - 运行中：pod已经被调度到某节点，并且所有容器已经被kubelet创建完成
  - 成功：pod中的所有容器都已经成功终止并且不会被重启
  - 失败：所有容器都已经终止，但至少有一个容器终止失败。
  - 未知：apiserver无法正常获取到pod对象的状态信息，通常是网络通信失败导致的
  ### 6.4 钩子函数
  ### 6.5 容器探测
  >容器探测用于检测容器中的应用实例是否正常工作，如果实例的状态不符合预期，那么k8s就会把该问题实例摘除
  - 存活性探针：检测应用实例当前是否处于正常运行状态
  - 就绪性探针：探测应用当前是否可以接受请求
  ### 6.6 重启策略
  - always:容器失效时，自动重启该容器
  - onFailure:容器终止运行且退出码不为0 
  - never:不论状态是什么，都不重启该容器
  ### 6.7 pod调度
  - 自动调度：运行在哪个节点上完全由Scheduler经过一系列算法计算得到
  - 定向调度：NodeName,NodeSelector'
  - 亲和性调度：NodeAffinity,PodAffinity,PodAffinity
  - 污点调度:Taints,Toleration
---
## 七、Controller
  >控制器，通过它来实现pod的管理，比如启动，停止pod，伸缩pod的数量等
  ### 7.1 Deployment
  >Deployment是pod控制器的其中之一,k8s很少直接控制pod,都是通过pod控制器操作
---
## 八、Service
  >pod对外服务的统一入口
---
## 九、Label
  >label用于对pod进行分类，实现对资源的分组，方便进行资源分配，调度，部署等工作
  ### 9.1 label的特点如下：
  - 一个label会以key-value键值对的形式附加在各种对象上，比如Node,Pod,Service
  - 一个资源对象可以定义任意数量的label,同一个label也可以被添加到任意数量的资源对象上去
  ### 9.2 常见的label示例：
  - 版本标签："version":"release"/"stable"
  - 环境标签:"environment":"dev"/"test"/"prod"
  - 架构标签："tier":"frontend"/"backend"
---
  

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
  ## 4.nginx服务调用实例
  - 第一步：k8s启动，mster,node将自己的信息存储在etcd数据库中
  - 第二步：nginx安装服务请求会被发送到master节点的apiServer组件
  - 第三步：apiServer组件调用scheduler组件，决定nginx服务安装到哪个node节点上
  - 第四步：apiServer调用controller-manager去调度Node节点，来安装nginx服务
  - 第五步：kubelet接到指令后，会通知docker，然后由docker来启动一个nginx的pod,pod是k8s的最小操作单元，容器必须跑在pod中
  - 第六步：nginx服务运行成功，如果需要访问nginx，需要通过kube-proxy来对pod产生访问代理，这样就可以访问集群中的nginx服务
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

