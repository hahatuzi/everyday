## LangChain的三个核心组件
  - Components组件：为LLMs提供接口封装，模版提示和信息检索索引
  - Chains链：它将不同的组件结合起来解决特定任务，比如在大量文本中查找信息
  - Agents代理：它们让llms能够与外界进行交互，比如通过API请求执行操作
## LangChain核心
  - 模型Models:大模型
  - Prompt Templates:提示模版
  - Chains
  - Agents
  - Embedding嵌入与向量索引VectorStore,它们是数据表示与检索的手段，为模型提供必要的语言理解基础
  - indexes:索引，能够帮助你从语言模型中提取相关信息
## LangChain底层原理
  用户提问-->通过相似性搜索在数据库或者向量空间中找到相关的信息-->由处理模型分析，产生答案-->
## LangSmith