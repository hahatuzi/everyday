  ### useState和useReducer之间的关系


# ReactDOM
  ### react内部的3个阶段：
   - schedule阶段：调度更新阶段
   - render阶段：workLoop --> beginWork,completeWork：处理更新阶段
   - commit阶段(commitWork),包含三个子阶段：befreMutation阶段，mutation阶段，layout阶段

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

# 实现多个原生标签子节点渲染的源码
  import type
# 实现文本节点的渲染