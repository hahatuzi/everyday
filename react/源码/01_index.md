# multirepo和monorepo的区别
# react项目结构
# 一：jsx转换
  ### 1.实现jsx方法
  - jsxDEV(dev环境)
  - jsx方法(prod环境)
  - React.createElement方法
  ### 2.实现打包流程：针对上述3个方法打包对应文件
  - react/jsx-dev-runtime.js(dev环境)
  - react/jsx-runtime.js(prod环境)
  - react
  ### 3.实现调试打包结果的环境


# 二：reconciler
  ### 1.ReactElement
  ReactElement如果作为核心模块操作的数据结构，存在以下问题：
  - 无法表达节点之间的关系
  - 字段有限，不好扩展
  所以需要一种新的数据结构，也就是FiberNode
  ### 2.FiberNode
  fiberNode是虚拟DOM在react中的实现方式。vue中叫VNode。它介于React Element和真实UI节点之间，能够表达节点之间的关系。转换过程为JSX --> ReactElement --> FIberNode--> DomElement
  ### 3.reconciler的工作方式
  对于同一个节点，比较其ReactElement与fiberNode,生成子fiberNode,根据比较结果生成各种标记（插入，删除，移动。。）
  ```js
  // 举例：挂载div
  // jsx('div') ---> (和对应的fiberNode) null --->  生成fiberNode --> 对应的标记 Placement
  // 将div更新为P
  // jsx(p) ---> fiberNode type:'div' --> 生成子fiberNode --> 对应标记 Deletion Placement
  ```
  ### 4.双缓冲技术
  当所有ReactElement比较完毕后，会生成一颗fiberNode树，项目一共存在两棵fiberNode树：current，workProgress。
  - current：对应真实UI的fiberNode树。
  - workProgress:触发更新后，正在reconclier中计算的fiberNode树
# jsx消费的顺序:DFS深度优先遍历的顺序遍历ReactElement，所以组件销毁的时候子组件优先被销毁


# 三：更新机制
  ### 1.常见触发更新的方式：
  - ReactDom.createRoot().render
  - this.setState
  - useState的dispatch
  ### 更新机制的组成部分
  - update：代表更新的数据结构
  - UpdateQueue:消费update的数据结构,UpdateQueue队列中包含多个sharePending,sharePending又是由多个update组成。
  ### 更新机制的工作流程
  - 实现mount时调用的API
  - 将该API接入上述更新机制中

fiberRootNode ----current----> hostRootFiber ----child----> APP ----return----> hostRootFiber ----stateNode----> fiberRootNode

# 四：首屏渲染的更新
# 五：初探mount流程
  更新流程的目的：生成wrip fiberNode树。
  进入A的beginWork --> 对比B的currentfiberNode和B的reactElement --> 生成B对应的Wrip 