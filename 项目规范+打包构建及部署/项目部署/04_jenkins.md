# jenkins三大概念：
  #### 一：Job(任务)
  在jenkins平台中，都是以job任务的形式完成一件事情。
  #### 二：plugins(插件)
  #### 三：workspace(工作空间)
  jenkins是通过本地文件的形式来存储和管理数据的。jenkins下的每一个job都有属于自己的workspace,用来存放本任务涉及到的数据和文件
# jenkins创建job

# jenkins pipeline,包括声明式pipeline和脚本式pipeline
#### pipeline包括声明式脚本和脚本式语法
概念：pipeline是一套运行在jenkins上的工作流框架，将原来独立运行于单个或者多个节点的任务连接起来，实现单个任务难以完成的复杂流程编排和可视化的工作。
pipeline脚本是有groovy语言实现的。
声明式：
```js
pipeline{ // 声明
  agent //'在哪个节点上构建',
  stages:{
    // 阶段，包含所有的任务步骤
    stage("scan"){
      steps{
        // 步骤，具体的任务步骤
      }
    }
  }
  post{
    // 任务完成之后的处理，比如发送邮件等
  }
}
```
agent:代理
stages：阶段
checkout阶段
shell编译阶段
![jenkins声明式语法]https://blog.csdn.net/zhou920786312/article/details/125955704
# Jenkins的常见的内置构建触发器
1.构建触发器：构件方式包括：**定时构建**，**远程构建**，**github触发器**，**源码变更构建**
定时构建的分类包括：分钟(0-59)，小时(0-24)，每月的天数，月数，一周的天数(0-7)
比如：每天晚上20点自动构建：0 20 * * *,*表示取有效期的所有值，-表示连续的时间段
每周二，周四的晚上8点执行 0 20 * * 2,4
每周二至周四的晚上8点执行 0 20 * * 2-4
轮询SCM:定时扫描本地仓库的代码是否有边锋，如果代码有变更就会触发
轮询SCM可以实现Gitlab代码更新，项目自动构建，但是该方案的性能不佳，当项目代码量比较大时构建时间比较长。所以采用了更好的方案：利用Gitlab的webhook实现代码push到仓库时立即触发项目的自动构建
轮询SCM原理示意图
Jenkins  --发送定时请求-->  Gitlab代码变更
Gitlab代码变更  --push完毕后发送构建请求-->  Jenkins
# Jenkins全局变量
env可以在声明式流水线中访问的环境变量，例如${env.PATH}或者${env.BUILD_ID}.
访问内置的全局变量参考页面${YOUR_JENKINS_URL}/pipeline-syntax/globals以获取完整的最新的，可用于流水线的环境变量列表。
currentBuild
可用于发现当前正在执行的流水线的信息，比如result,displayName等属性。
# Jenkins环境变量environment
(1)最外层，用在最外层的pipeline块中的enviroment指令用于流水线的所有步骤
(2)stage中，定义在stage中的enviorment指令只适用于stage中的步骤。
pipeline{
  enviorment{

  }
  stages{
    stage(){
      environment{

      }
    }
  }
}