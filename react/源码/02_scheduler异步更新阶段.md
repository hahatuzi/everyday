# schedule --> Reconciler --> render
# schedule阶段：调度更新阶段
  > 页面初次渲染，类组件setState,forceUpdate,函数组件的**setState**都会**调用scheduleUpdateOnFiber进行更新**。
  > 标记根节点有一个pending update,即待处理的更新：markRootUpdated
  > ensureRootIsScheduled： 每次root:FiberRoot接收update的时候都会调用它，确保有一个待处理的微任务来处理根调度
  ### 协调的目的：构建新的子fiber结构，检查是否有老fiber,如果有，检查是否可以复用
  ### 工作流程
  ReactDOM.render --> createRoot --> updateContainer --> scheduleUpdateOnFiber --> ensureRootIsScheduled --> performSyncWorkOnRoot --> prepareFreshStrack --> createWorkInProgress --> commitRoot --> commitMutationEffects --> commitMutationEffectsOnFiber --> commitPlacement/commitUpdate/commitDeletion/commitPassiveEffect

  ```js
    // 在fiebr中调度update
    export function scheduleUpdateOnFiber (fiber:FiberNode, lane:Lane) {
      const root = markUpdateFromFiberToRoot(fiber)
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

  ### 删除单个节点
    ```js
      function deleteChild (returnFiber:FiberNode, childToDelete:FiberNode) {
        if(!shouldTrackEffects){
          return
        }
        const deletions = returnFiber.deletions
        if(deletions === null){
          returnFiber.deletions = [childToDelete]
          returnFiber.flags |= ChildDeletion
        } else {
          deletions.push(childToDelete)
        }
      }
    ```

# 重点概念：
实现调度requestIdealCallback
  ### Heap
  ###