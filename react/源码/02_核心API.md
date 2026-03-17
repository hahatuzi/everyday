# 核心API
  - useState
  - useReducer
  - useCallback
  - useMemo
  - useRef
  - createContext,Provier
  - createElement
  
# 代码分析
  useState --> dispatcher.useState() --> resolveDispatcher() --> ReactCurentDispatcher.current --> HooksDispatcherOnmount/ HooksDispatcherOnUpdate
  --> mountWorkInProgressHook() --> hook --> queue --> dispatchSetState --> requestUpdateLan(fiber) --> enqueueConCurrentHookUpdate() -->
  scheduleUpdateOnFiber(root,  fiber,  lane, eventTime),entangTransitionUpdate(root, queue, lane)
  ### useState分析
  mountWorkInProgressHook --> basicStateReducer --> 
  ### useState和useReducer之间的关系

# reconclier
  ### FiberRoot
  dispatchSetState --> fiber --> mountState(无fiber) --
  ### RootFiber
  createHostRootFiber
# React Hook
  ### completeWork需要解决的问题：
    - 对于Host类型fiberNode:构建离屏DOM树
    - 标记Update flag
  ### completeWork性能优化策略
   - flags分布在不同的fiberNode中，如何快速找到他们？：利用completeWork向上遍历的流程，将子fiberNode的flags冒泡到父fiberNode

# ReactDOM
  ### react内部的3个阶段：
   - schedule阶段：调度更新阶段
   - render阶段：workLoop --> beginWork,completeWork：处理更新阶段
   - commit阶段(commitWork),包含三个子阶段：befreMutation阶段，mutation阶段，layout阶段

# 事件系统：
  模拟浏览器事件捕获，实现合成事件对象
  - 实现reactDOM和reconcoler对接：
  将事件毁掉保存在DOM中，通过创建DOM和更新属性时对接