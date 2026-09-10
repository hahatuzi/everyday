# index

---

## 目录

1. [node](#一、node)
2. [Node的事件循环](#二、Node的事件循环)
3. [jenkins项目构建](#三、jenkins项目构建)
4. [jenkins配置](#四、jenkins配置)
5. [Jenkins安装方式](#五、Jenkins安装方式)
6. [jenkins配置](#六、jenkins权限管理)
7. [Jenkins部署步骤](#七、Jenkins部署步骤)

---

## 一、node
  > node可以用来干嘛？用 Express / Koa / NestJS 写 RESTful 接口，处理业务逻辑、操作数据库
  ### 1.1 npm和pnpm的区别
  > npm：Node.js 官方自带包管理器；pnpm：第三方高性能包管理器，**绝大多数命令和 npm 兼容**。核心差异来自底层 `node_modules` 的实现机制，下面用通俗例子 + 对比。
  #### (1)底层存储机制（最核心区别）
    - npm
      - 把依赖尽量复制到项目根目录 `node_modules`，每个项目**独立复制一份包文件**。
      - 同一个版本的包，10 个项目就会复制 10 份，**磁盘占用高**。
    - pnpm
      - 内容寻址存储 CAS + 硬链接 + 符号链接。全局有一个统一仓库 `~/.pnpm‑store`，**同一个版本包磁盘只存 1 份**。
      - 项目 `node_modules` 不复制真实文件，而是**硬链接指向全局仓库**，几乎不额外占磁盘。
      - 内部 `.pnpm` 目录存放真实链接；根目录只放你**显式声明的依赖**。
  #### (2)性能对比
    - 冷启动：差距不大
    - 热安装(已经有缓存时)，pnpm只创建链接，速度远快于npm
    - 删完 node_modules，pnpm install 几秒完成；npm 要等很久。
  #### (3)Monorepo（多包仓库）
    - npm：支持 workspace，但配置简陋，体验一般。
    - pnpm：**原生 workspace，pnpm‑workspace.yaml**，业界主流方案，适合大型多包项目。
## 二、Node的事件循环
  ### 1.宏任务
  - setTimeout
  - setInterval
  - IO事件
  - setImmediate
  - close事件
  ### 2.微任务
  微任务其实可以划分为**next tick queue**和**other queue**两种，process.nextTick是next tick queue,process.nextTick,queueMicrotask属于other queue
  - Promise.then
  - process.nextTick
  - queueMicrotask
  ### 3.执行顺序：同步代码-->处理process.nextTick()队列 -->处理其他微任务-->开始事件循环的各个阶段
  ### 4.node事件循环的各个阶段
  - **（1）timers定时器**：执行setTimeout,setInterval的回调函数
  - **（2）Pending callbacks待定回调**：处理上一轮循环中未完成的IO任务，比如被拒绝的TCP链接
  - **（3）Idle,prepare空闲准备**：只用于系统内部调用
  - **（4）Poll轮询**：等待新的IO事件，执行IO回调，处理poll队列中的事件
  - **（5）Check检查**：执行setImmediate的回调
  - **（6）Close callback关闭回调**：处理socket.on(‘close’)的回调函数