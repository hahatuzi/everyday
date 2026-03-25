# useState
  ```js
    function mountState<State>(initialState:(()=> State | State)):[State,Dispatch<State>]{
      const hook = mountWorkInprogressHook()
      let memoizedState
      if(initialState instanceof Function){
        memoizedState = initialState()
      } else {
        memoizedState = initialState
      }

      const queue = createUpdateQueue<State>()
      hook.updateQueue = queue

      const dispatch = dispatchSetState.bind(null, currentlyRenderingFiber, queue)
      queue.dispatch = dispatch
      return [memoizedState, dispatch]
    }
    
    function dispatchSetState<State>(fiber:FiberNode, updateQueue:UpdateQueue<State>, action:Action<State>){
      const lane = requestUpdateLane()
      const update = createUpdate(action, lane)
      enqueueUpdate(updateQueue, update)
      scheduleUpdateOnFiber(fiber, lane)
    }
  ```