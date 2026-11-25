## 一、LangGraph入门
  ### 1.1 基本概念
  > 图Grapth是由Edge和Node组成的按照特定顺序执行的工作流。输入是state,输出的是加工后的state，所以图就是加工处理state的流水线
  - **状态**：整个工作流中流转的数据
  - **节点**：工作流中的关键 工作步骤，用函数来定义，主要任务是加工处理State中的数据
  - **边**：把各个节点连接起来的路径，是控制工作流走向的关键
  ### 1.2 节点Node
  > 节点是图的执行单元，用来加工数据，多数情况下节点就是一个Python函数
  ```py
    def my_node(state:State) -> dict :
      # c从state读取数据，执行计算逻辑（可以调用LLM,工具，数据库等）
      return {"age":new_age}
  ```
  ### 1.3 自定义Reducer
  ```py
    def add_reducer(old, new):
      return old + new
    class CustomReducerState(TypeDict):
      count: int
      nodes: Annotated[list[str], add_reducer]
  ```
  ### 1.4 边
  > 边可以定义图中节点的执行顺序，连接节点，形成图
  - normal edge:串行和并行
  - conditional edge