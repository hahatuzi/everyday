
# unmount
  ### flushSync:允许你强制 React在提供的毁掉函数中同步刷新任何更新，这将确保DOM立即更新

# update
  # Update, SharedQueue, UpdateQueue类型定义
    ```js
      export interface Update<State>{
        action:Action<State>,
        lane:Lane,
        next:Update<any> | null
      }
      export interface UpdateQueue<State>{
        shared:{
          pending: Update<State> | null
        };
        dispatch:Dispatch<State> | null
      }
    ```
  ### markUpdateLaneFromFiberToRoot
  ### processUpdateQueue
  processUpdateRoot在beginWorks阶段会被两个地方调用：updateHostRoot,updateClassComponent

