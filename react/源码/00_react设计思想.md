# react设计思想
  ### 第一步：react初始化挂载
    react初始化挂载-->render-->createContainer(构建fiberRootNode和hostRootFiber)-->构建内存图-->fiberRootNode和hostRootFIber
  ### 第二步：初始化事件
    初始化事件-->将事件都绑定在根节点上--> dispatch代理根节点上的各种事件
  ### 第三步：updateContainer开始渲染
    updateContainer开始渲染-->获取当前渲染的优先级-->创建Update对象-->ection代表App Element对象，next包含action和当前更新优先级，update是环状链表
  ### 第四步：scheduleUpdateOnFiber开始调度渲染
    updateContainer开始渲染-->markUpdaeFIberOnFiberToRppt找到根节点-->markRootUpdated修改根节点的pendingLanes，确认本次渲染的优先级
  ### 第五步：ensureRootIsScheduled确认当前调度为同步还是并发调度
  getHighestPriontyLane获取最高优先级的任务-->如果是同步优先级，向微任务中添加performSyncWorkOnRoot任务，传入root和优先级，V18默认是同步渲染，并发需要单独开启
  ### 第六步：进入performSyncWorkOnRoot
  获取最高优先级-->（如果不是当前优先级，进入ensureRootISScheduled）优先符合同步优先级要求-->进入render阶段prepareFreshStack进行初始化
  ### 第七步：commit流程
  