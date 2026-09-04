## LangChain的三个核心组件
  - Components组件：为LLMs提供接口封装，模版提示和信息检索索引
  - Chains链：它将不同的组件结合起来解决特定任务，比如在大量文本中查找信息
  - Agents代理：它们让llms能够与外界进行交互，比如通过API请求执行操作
## LangChain核心
  - 模型Models:大模型
  - Prompt Templates:提示模版
  - Chains
  - Agents
  - Embeddings:嵌入与向量索引VectorStore,它们是数据表示与检索的手段，为模型提供必要的语言理解基础
  - indexes:索引，能够帮助你从语言模型中提取相关信息
## Embeddings
  > 将文本转成一组N维浮点数，即文本向量又叫Embeddings,向量之间可以计算距离，距离远近又叫语义相似度大小
  - 欧式距离计算法
  - 余弦距离计算法
  ### 步骤：
  - 第一步：Indexing:load file--> split --> embed --> store
  - 第二步：Retrieval & Generation: question --> retrieve --> prompt --> LLM --> answer
## LangChain底层原理
  用户提问-->通过相似性搜索在数据库或者向量空间中找到相关的信息-->由处理模型分析，产生答案-->
## LangSmith
## conda使用指南
  ```js
  // conda创建一个名字叫langchain1.3的环境,指定python版本为3.14.5
  conda create --name langchain1.3 python=3.14.5
  // conda查看安装好的环境列表
  conda env list
  // conda 初始化虚拟环境
  conda init
  // 切换到某python环境
  conda activate langchain1.3
  // 验证python版本
  python --version
  // =======================================
  // 下载langchain安装包
  // =======================================
  // 安装指定版本的langchain,比如1.3.15
  conda install langchain==1.3.15
  // 或者安装最新版
  conda install langchain
  // 指定频道
  conda install -c conda-forge langchain==1.3.15
  // 更新包
  conda update langchain
  // 卸载包
  conda uninstall langchain
  // 查看已经安装的包
  conda list
  ```
  ### conda和pip的区别
  - conda依赖检查严格，pip相对宽松
  - conda负责环境+依赖+稳定性，pip只负责python包
  - conda支持python包和非python包，pip只支持python包