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