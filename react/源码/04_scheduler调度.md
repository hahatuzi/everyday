# 一：scheeduler调度器
  ### 1.scheduler核心流程
    ```js
      // Scheduler核心工作流程示意
      function workLoop(hasTimeRemaining, initialTime) {
        let currentTime = initialTime;
        return function performUnitOfWork(unitOfWork) {
          // 执行单个工作单元
          const next = unitOfWork.perform();
          // 检查是否需要让出主线程
          if (needsYieldToHost() || !hasTimeRemaining) {
            return next;
          }
          // 继续处理下一个工作单元
          return performUnitOfWork(next);
        };
      }
    ```
  ### 2.scheduler调度器的的核心功能：
  - (1)时间切片，解决UI卡顿问题
    >  JS的单线程会导致长任务阻塞主线程，导致UI卡顿和用户交互延迟，所以出现了scheduler调度器，将任务分解成不超过浏览器一帧（通常16ms）的片段，每一帧结束后让出主线程，优先处理用户输入等优先级较高的任务。时间切片的本质是模拟实现requestIdleCallback
    - useDeferredValue：延迟更新低优先级状态
    - useTransition：标记状态更新为非阻塞过渡
    - startTransition：将计算密集型任务标记为过渡任务
  - (2)并发模式下的任务优先级调度:
    - ImmediatePriority：紧急任务，需立即执行（如**用户输入**）
    - UserBlockingPriority：用户交互相关任务（如**动画**、滚动）
    - NormalPriority：普通优先级（如**数据获取**）
    - LowPriority：低优先级任务（如非紧急数据处理）
    - IdlePriority：空闲时执行的任务（如**日志记录**）

# 二：优先级调度：
  ### 1.scheduler的优先级处理策略：不同的优先级任务有不同的expirationTime(过期时间) 
  - timerQueue：保存未过期任务，timerQueue中任务过期时取出放在taskQueue中
  - taskQueue:保存已过期任务
  ### 2.小顶堆：实现优先级队列，为了能找到任务队列中最早的那个任务


# 三：schedule阶段：调度更新阶段
  > 页面初次渲染，类组件setState,forceUpdate,函数组件的**setState**都会**调用scheduleUpdateOnFiber进行更新**。
  > 标记根节点有一个pending update,即待处理的更新：markRootUpdated
  > ensureRootIsScheduled： 每次root:FiberRoot接收update的时候都会调用它，确保有一个待处理的微任务来处理根调度
  ### 1.协调的目的：构建新的子fiber结构，检查是否有老fiber,如果有，检查是否可以复用
  ### 2.工作流程
  ReactDOM.render --> createRoot --> updateContainer --> scheduleUpdateOnFiber --> ensureRootIsScheduled --> performSyncWorkOnRoot --> prepareFreshStrack --> createWorkInProgress(处理节点) --> commitRoot --> commitMutationEffects --> commitMutationEffectsOnFiber --> commitPlacement/commitUpdate/commitDeletion/commitPassiveEffect

    ```js
      // 在fiebr中调度update,hostRootFiber开始渲染
      export function scheduleUpdateOnFiber (fiber:FiberNode, lane:Lane) {
        const root = markUpdateFromFiberToRoot(fiber) //获取根节点
        markRootUpdated(root,lane) // 标记根节点有一个pending update,即待处理的更新
        ensureRootIsScheduled(root)
      }

      function ensureRootIsScheduled (root:FiberRootNode) {
        const updateLane  = getHighestPriorityLane(root.pendingLanes)
        if(updateLane === NoLane){
          return
        }
        if( updateLane === SyncLane){
          // 同步优先级，用微任务调度
          if (__DEV__){
            console.log('在微任务中调度,优先级:', updateLane)
          }
          // 任务调度器的入口函数
          // [performSyncWorkOnRoot, performSyncWorkOnRoot, performSyncWorkOnRoot]
          scheduleSyncCallback(performSyncWorkOnRoot.bind(null, root, updateLane))
          scheduleMicroTask(flushSyncCallbacks)
        } else {
          // 其他优先级，用宏任务调度
        }
      }
      function markRootUpdated (root:FiberRootNode, lane:Lane) {
        root.pendingLanes = mergeLanes(root.pendingLanes, lane)
      }
      export function scheduleSyncCallback (callback:(...args:any) => void) {
        if (syncQueue === null) {
          syncQueue = [callback]
        } else {
          syncQueue.push(callback)
        }
      }
    ```
  ### 3.异步可中断更新和饥饿问题