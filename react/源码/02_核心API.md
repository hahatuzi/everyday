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
  ```js
    const [age, setAge] = useState(1)
    function increment () {
      setAge(age + 1)
    }
    <button onClick={() => {
      increment()
      increment()
      increment()
    }}></button>
    // 2,setAge多次调用，会进行合并，最终只触发一次更新，如果想要调用多次，可以改成setAge(age => age + 1)
  ```
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

   ### completeWork流程
   主要处理"标记update"的情况
  ### commitWork流程：
  对于标记ChildDeletion的子树，由于子树中：
  - 对于FC,需要处理useEffect unmount的执行，解绑ref
  - 对于HostComponent,需要解绑ref
  - 对于子树的"根HostComponent",需要移除DOM
  所以需要实现遍历childDeletion子树的流程

  ### useState:
  需要实现：
  - 针对update的dispatcher
  - 实现对标mountWorkInProgress的updateWorkInProgressHook
  - 实现updateState中的计算新state的逻辑
  其中updateWorkInProgress的实现需要考虑的问题：
  - hook数据从哪里来？
  - 交互阶段触发的更新

# useState的mount和update流程的区别
  ### beginWork：
  - 需要处理childDeletion的情况
  - 需要处理节点移动的情况
  ### completeWork：
  - 需要处理HostText内容更新的情况
  - 需要处理HostComponent属性变化的情况
  ### commitWork:
  - 对于ChildDeletion,需要遍历被删除的子树
  ### useState：
  - 实现相对于mountState的updateState
# 事件系统：
  模拟浏览器事件捕获，实现合成事件对象
  - 实现reactDOM和reconcoler对接：
  将事件毁掉保存在DOM中，通过创建DOM和更新属性时对接

# 实现多个原生标签子节点渲染的源码
  import type
# 实现文本节点的渲染