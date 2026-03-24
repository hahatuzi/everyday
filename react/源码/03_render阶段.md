# render阶段
  > 流程：performConcurrentWorkOnRoot --> renderRootSync --> workLoopSync --> performUnitOfWork --> beginWork --> completeUnitOfWork --> completeWork
  performConcurrentWorkOnRoot这个函数中有两个重要的阶段：render和commit
  ### 1.render阶段的过程
   - (1)executionContext |= RenderContext
   - (2)workInProgressTransitions赋值getTransitionForLane(root,lanes)
   - (3)**prepareFreshStack**初始化
   - (4)workLoopSync，**从根节点开始遍历Fiber树**，perfromUnitOfWork(beginWork更新当前fiber,比如props,state更新，生命周期函数执行，hooks函数执行等，返回下一个fiber, complateUnitOfWork)
   - (5)workInProgressX,workInProgress已经在preformUnitWork阶段更新
   - (6)再遍历一遍更新队列，finishQueueingConcurrentUpdates()
  ### beginWork
  beginWork --> reconcileChildren --> createChildReconciler

  ### renderRootConcurrent

  ### completeWork
  commitMutationEffects --> commitMutationEffectsOnFiber --> 