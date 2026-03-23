# render
  ### createRoot函数
   ```js
    /**
     * createRoot
    *
    * @param {Container} container
    * @param {CreateRootOptions} options
    * @returns {RootType} reactDOMRoot的实例
    */
    function createRoot(container:Container, options?:CreateRootOptions): RootType{
      const root = createContainer(container)

      return {
        render(element:ReactElementType){
          initEvent(container, 'click')
          updateContainer(element,root)
        },
        unmount(),
        _internalroot
      }
    }
   ```
  ### createContainer,updateContainer
  createRoot --> updateContainer(处理优先级更新队列) --> createUpdate(lane,next,acion) --> updateQueue
  ```js
    // reactDOM.createRoot()内部执行createContainer，创建整个应用的根节点fiberrootNode
    export function createContainer(container:Container){
      const hostRootFiber= new FiberNode(HostRoot, {}, null)
      const root = new FiberRootNode(container, hostRootFiber)
      hostRootFiber.updateQueue = createUpdateQueue()
      return root
    }
    // reactDOM.createRoot().render执行updateContainer,将首屏渲染和更新机制联系在一起
    export function updateContainer(
      element:ReactElementType | null,
      root:FiberRootNode
    ){
      const hostRootFiber = root.current
      const lane = requestUpdateLane() // 页面初次渲染，defaultLane
      // 每一个update都会被分配一个或者多个lane,以确保他在更新队列中的优先级顺序
      const update = createUpdate<ReactElementType | null>(element, lane)
      enqueueUpdate(
        hostRootFiber.updateQueue as UpdateQueue<ReactElementType | null>,
        update
      )
      // 开始调度
      scheduleUpdateOnFiber(hostRootFiber)
      return element
    }
  ```
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


# scheduleUpdateOnFiber调度更新:
  - 页面初次渲染，类组件setState,forceUpdate,函数组件的setState都会调用scheduleUpdateOnFiber进行更新
  - 标记根节点有一个pending update,即待处理的更新：markRootUpdated
  - ensureRootIsScheduled： 每次root:FiberRoot接收update的时候都会调用它，确保有一个待处理的微任务来处理根调度
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
  ```