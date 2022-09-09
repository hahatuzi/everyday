# pipeline包括声明式脚本和脚本式语法
概念：pipeline是一套运行在jenkins上的工作流框架，将原来独立运行于单个或者多个节点的任务连接起来，实现单个任务难以完成的复杂流程编排和可视化的工作。
pipeline脚本是有groovy语言实现的。
声明式：
agent:代理
stages：阶段
checkout阶段
shell编译阶段
# Jenkins的常见的内置构建触发器
轮询SCM:定时扫描本地仓库的代码是否有边锋，如果代码有变更就会触发
轮询SCM可以实现Gitlab代码更新，项目自动构建，但是该方案的性能不佳，当项目代码量比较大时构建时间比较长。所以采用了更好的方案：利用Gitlab的webhook实现代码push到仓库时立即触发项目的自动构建
轮询SCM原理示意图
Jenkins  --发送定时请求-->  Gitlab代码变更
Gitlab代码变更  --push完毕后发送构建请求-->  Jenkins