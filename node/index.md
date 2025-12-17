# 一：Node的事件循环
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