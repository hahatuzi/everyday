# useEffect
  ## useEffect回调的执行过程
  commit之前
  ```js
    function mountEffect (create:EffectCallback | void, deps:EffectDeps) {
      const hook = mountWorkInprogressHook()
      const nextDeps = deps === undefined ? null : deps;
      (currentlyRenderingFiber as FiberNode).flags |= PassiveEffect


      hook.memoizedState = pushEffect(Passive | HookHashEffect, create, undefined,nextDeps )
    }
    function updateEffect (create:EffectCallback | void, deps:EffectDeps) {
      const hook = updateWorkInProgressHook()
      const nextDeps = deps === undefined ? null : deps;
      (currentlyRenderingFiber as FiberNode).flags |= PassiveEffect


      hook.memoizedState = pushEffect(Passive | HookHashEffect, create, undefined,nextDeps )
    }
  ```