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
  ### 1.fiberNode是虚拟DOM在react中的实现方式，它介于React Element和真实UI节点之间，能够表达节点之间的关系。JSX --> ReactElement --> FIberNode--> DomElement
  ### 1.reconciler的工作方式
对于同一个节点，比较其reactElement与fiberNode,生成子fiberNode,根据比较结果生成各种标记
# jsx消费的顺序:DFS深度优先遍历的顺序遍历ReactElement，所以组件销毁的时候子组件优先被销毁