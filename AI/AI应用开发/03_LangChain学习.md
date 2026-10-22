## 目录

1. [LangChain基础](#一、LangChain基础)
2. [Embedding向量化](#二、LangChain调用大模型)
3. [LangChain的提示词模版PromptTemplate类](#三、LangChain的提示词模版PromptTemplate类)

---
## 一、LangChain基础
  ### 1.1 LangChain的三个核心组件
     - Components组件：为LLMs提供接口封装，模版提示和信息检索索引
     - Chains链：它将不同的组件结合起来解决特定任务，比如在大量文本中查找信息
     - Agents代理：它们让llms能够与外界进行交互，比如通过API请求执行操作
  ### 1.2 LangChain核心功能
    - Prompts：优化提示词
    - Models：调用各类模型
    - History管理会话历史记录
    - indexs:管理和分析各类文档，能够帮助你从语言模型中提取相关信息
    - Chains：构建功能的执行链条
    - Embeddings:嵌入与向量索引VectorStore,它们是数据表示与检索的手段，为模型提供必要的语言理解基础
  ### 1.3 LangChain安装
  > pip install langchain langchain-community langchain-ollama dashscope chromadb
    - langchain-community:社区支持包，提供了更多的第三方模型调用
    - dashscope:阿里云通义千问的PythonSDK
    - chromadb:轻量向量数据库

  ### 1.4 LangChain底层原理
  > 用户提问-->通过相似性搜索在数据库或者向量空间中找到相关的信息-->由处理模型分析，产生答案-->

## 二、LangChain调用大模型
  > LangChain支持的模型：LLMS(大语言模型),ChatModels(聊天模型),Embeddings Models(嵌入模型)
  ### 2.1 调用LLMS模型
  ```py
    # (1)langchain调用千问模型
    from langchian_community.llms.tongyi import Tongyi
    llm = Tongyi(model = 'qwen-max')
    res = llm.invoke('帮我做个作业吧')
    # (2)langchain调用本地大模型
    from langchain_ollama import OllamaLLM
    model = OllamaLLM(model="qwen3:4b")
    res = model.invoke(input = '你是谁？')
    print(res)
  ```
  ### 2.2 langchain调用聊天模型
  ```py
    from langchian_community.llms.tongyi import Tongyi
    from langchain_core.messages import  HumanMessage,SystemMessage,AIMessage
    chat = Tongyi(model = 'qwen3-max')
    messages = [
      SystemMessage(content = '你是一位来自边塞的诗人'),
      HumanMessage(content = '帮我的小店些一首诗吧'),
      AIMessage(content = 'XXX'),
      # 或者('ai',content='XXX')
      HumanMessage('根据你上面的诗歌格式再写一首吧')
    ]
    for chunk in chat.tream(input = message):
      print(chunk.content, end = '', flush=True)
  ```
  ### 2.3 LangChain调用Embedding Model文本嵌入模型
  ```py
    # 将文本作为输入，转化为一个浮点列表向量
    from langchain_community.embeddings import DashScopeEmbeddings
    model = DashScopembeddings()
    print(model.embed_query('我喜欢你'))
    print(model.embed_documents(['我爱你','我喜欢你']))
  ```
  ### 2.4 模型的流式输出
  > model.invoke：一次性输出返回结果
  > model.stream:流式输出
  ```py
    from langchain_ollama import OllamaLLM
    model = OllamaLLM(model="qwen3:4b")

    res = model.stream(input = '你是谁？')
    for chunk in res:
      print(chunk, end="",flush=True)
      # flush为直接刷新
  ```
---
## 三、LangChain的提示词模版PromptTemplate类
  > 该类用来协助优化提示词，支持变量的注入，可以构建一个自定义的基础提示词模版。包括PrmptTemplate通用提示词模版，FewShotPromptTemplate:支持基于模版注入任意数量的实例信息，ChatPromptTemplate:支持注入任意数量的历史会话信息
  > zero-shot思想下，可以基于PromptTemplate直接完成。few-shot思想下，需要更换为FewShotPromptTemplate
  ### 3.1 标准写法：PromptTemplete模版
  > from_template只能接入一条消息
  ```py
    from langchain_core.prompts import PromptTemplete
    from langchain_cmmunity.llms.tongyi import Tongyi

    prompt_template = PromptTemplate.from_template("我的邻居姓{lastname},刚生了个{gender},帮忙起个名字吧")
    prompt_text = prompt_template.format(name='章',gender="女儿")

    model = Tongyi(model="qwen-max")
    res = model.invoke(input=prompt_text)

    print(res)
  ```
  ### 3.2 FewShotPromptTemplate模版
  - example_prompt:示例数据的模版
  - exampes:实例样本
  - prefix:None,String,示例之前的提示词
  - suffix:示例之后的提示词
  - input_variables:声明在前缀或者后缀中所需要注入的变量名
  ```py
    from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
    example_template = PromptTemplate.from_template("词语：{word},它的反义词是{antoym}")
    example_data = [
      {"word":"大","antoym":"小"},
      {"word":"多","antoym":"少"},
    ]

    few_shot_template = FewShotPromptTemplate(
      example_prompt = example_template,
      examples = example_data,
      prefix = "告知我词语的反义词，我提供如下示例：",
      suffix = "基于前面的实例告诉我，{input_word}的反义词是什么？",
      input_variables = ["input_word"]
    )
    prompt_text = few_shot_template.invoke(input={"input_word":"左"}).to_string()
    print(prompt_text)
    model=Tongyi(model="qwen-max")
    print(model.invoke(input=prompt_text))
  ```
  ### 3.3 模版类的format和invoke方法
  | 区别 | **format** | **invoke** |
  |------|------|------|
  | 功能 | 纯字符串替换，解析占位符生成提示词 | Runnable接口标准方法，解析占位符生成提示词 |
  | 返回值 | 字符串 | PromptValue对象,需要通过to_string()转化 |
  | 传参 | .format(k=v,k=v) | .invoke({"k":v}) |
  | 解析 | 支持解析{}占位符 | 支持解析{}占位符和MessagePlaceholder结构化占位符 |
  ```py
    from langchain_core.prompts import PromptTemplate
    template = PromptTemplate.from_template("我的邻居是：{lastname},她喜欢{hobby}")
    res = template.format(lastname="lisa", hobby="pop")
  ```
  ### 3.4 ChatTemplate模板
  > ChatTemplate模板支持注入任意数量的历史会话信息
  > 通过from_messages方法，从列表中获取多轮次会话作为聊天的基础模版，PromptTemplate的from_template只能接入一条消息，而form_messages可以接入一个list的消息
  ```py
    from langchain_core.prompts import ChatPromptTemplate, MessagePlaceholder
    from langchain_cmmunity.llms.tongyi import Tongyi
    chat_prompt_template = ChatPromptTemplate.from_messages(
      [
        ("system":"你是一个边塞诗人，可以作诗。"),
        MessagePlaceholder("history"),
        ("human","请再来一首唐诗")
      ]
    )
    history_data = [
      ("human","你来写一首唐诗"),
      ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
      ("human","再来一首"),
      ("ai",'')
    ]
    prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
    model = Tongyi(model="qwen-max")
    res = model.invoke(input=prompt_text)

    print(res)
  ```
  ### 3.5 chain链式写法
  > 将组件串联，上一个组件额度输出作为下一个组件的输入，chain = prompt_template | model,必须都是Runnable的子类对象才能入链
  > invoke/stream → 字典{“history":history_data} → chat_prompt_template → 提示词文本 → 模型调用，生成消息对象
  ```py
    from langchain_core.prompts import PromptTemplete
    from langchain_cmmunity.llms.tongyi import Tongyi

    prompt_template = PromptTemplate.from_template("我的邻居叫{},刚生了个{gender},帮忙起个名字吧")
    prompt_text = prompt_template.format(name='章',gender="女")

    model = Tongyi(model="qwen-max")
    chain = prompt_template | model

    res = chain.invoke(input=prompt_text)
  ```
---
## 四、Runnable知识点
  ### 4.1 Runnable接口
  > LangChain中绝大多数核心组件都继承了Runnable抽象类，位于langchain_core.runnables.base
  ### 4.2 StrOutParser字符串输出解析器
  > AIMessage → str
  > StrOutParser是Runnable的子类，可以将AIMessage解析为简单额字符串，符合了模型invoke方法的要求(可以穿字符串，不能是AIMessage)，
  ```js
    chain = prompt | model | model
    def invoke(
      self,
      input: LanguageModelInput,
      config:RunnableConfig | None = None,
      *,
    )
  ```
  ### 4.3 JsonOutputParser
  > AIMessage → Dict(JSON),目的是为了将模型输出的AImessage转为字典，然后注入第二个提示词模版中，形成新的提示词(PromptValue对象)
  > 在构建链的时候要注意整体的额兼容性，注意前后组件的输入和输出要求。
  - 模型输入：PromptValue或者字符串或者序列（BaseMessage,list,tuple,str,dict）
  - 模型输出：AIMessage
  - 提示词模版输入：要求是字典
  - 提示词模版输出:PromptValue对象
  - StrOutputParser:AIMessage输入，str输出
  - JsonOutputParser:AIMessage输入，dict输出
  - 
  ### 4.4 chain链格式要求
  → invoke/stream：字典
  → first_prompt:PromptValue
  → model:AIMessage
  → json_parser:字典
  → second_prompt：PromptValue
  → model：AIMessage
  → str_parser：字符串
  ### 4.5 RunnambeLamba
  > RunnambeLamba可以自己编写Lambda匿名函数来完成自定义逻辑的数据换转，RunnambeLamba是LangChain内置的，将普通函数等转换为Runnable接口实例，方便自定义函数加入chain
## 五、LangChain的临时记忆和长期会话记忆
  ### 5.1 临时记忆
  > 基于**RunnableWithMessageHistory**在原有链的基础上创建带有历史记录功能的新链(新的Runnable实例)
  > 基于**InMemoryChatMessageHistory**为历史记录提供内存存储
  ```py
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_core.chat_history import InMemoryChatMessageHistory
    
    chat_history_store = {} # 存放多个会话ID所对应的历史会话记录

    def get_history(session_id):
      if session_id not in chat_history_store:
          store[session_id] = InMemoryChatMessageHistory()
      return store[session_id]

    conversation_chain = RunnableWithMessageHistory(
      base_chain, # 被附加历史消息的Runnable，通常是chain
      get_history, # 该函数用于获取指定会话ID的历史会话
      input_messages_key="input", # 声明用户输入消息在模版中的占位符
      history_messages_key="chat_history",# 声明历史消息在模版中的占位符
    )
  ```
  ### 5.2 长期会话记忆
  > 使用InMemoryChatMessageHistory只能在内存中临时存储会话记忆。所以出现了FileChatMessageHistory类，基于文件存储会话记录
  - add_messages:同步模式，添加消息
  - messages:同步模式，获取消息
  - clear:同步模式，清除消息
  ```py
    import json
    from typing import Sequence

    from langchain_core.chat_history import BaseChatMessageHistory
    import os

    from langchain_core.messages import message_to_dict, BaseMessage, messages_from_dict


    class FileChatMessageHistory(BaseChatMessageHistory):
        def __init__(self, session_id, storage_path):
            self.session_id = session_id  # 会话id
            self.storage_path = storage_path # 不同会话id的存储文件，所在的文件夹路径
            # 完整的文件路径
            self.file_path = os.path.join(self.storage_path, self.session_id)
            # 确保文件夹是存在的
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        def add_messages(self, messages: Sequence[BaseMessage]) -> None:
            # sequence序列类似list,tuple
            all_messages = list(self.messages)
            all_messages.extend(messages)   # 新的和已有的组合成一个list
            # 将数据同步写入到本地文件中，类对象写入文件→二进制
            # 为了方便，可以将BaseMessage消息转换为字典，然后再使用json模块以json字符串形式写入文件
            # message_to_dict:单个消息对象(BaseMessage类实例)→字典

            # new_messages = []
            # for message in all_messages:
            #     d = message_to_dict(message)
            #     new_messages.append(d)

            new_messages = [message_to_dict(message) for message in all_messages]
            # 将数据写入文件
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump(new_messages, f)
        @property # @property装饰器将messages方法变成成员属性用
        def messages(self) -> list[BaseMessage]:
            # 当前文件内：list[字典]
            try:
                with open(self.file_path, 'r', encoding="utf-8") as f:
                    messages_data = json.load(f)
                    return messages_from_dict(messages_data)
            except FileNotFoundError:
                return []
        def clear(self) -> None:
            with open(self.file_path, 'w', encoding="utf-8") as f:
                json.dump([],f)
  ```
  ### 5.3 CVSLoader
  - load():一次性加载全部文档
  - lazy_load():延迟流式传输文档
  ```py
    loader = CSVLoader()
    documents = loader.load()
    for document in loader.lazy_load():
      print(document)
  ```
  ### 5.4 JSONLoader
  > 需要先pip install jq, 
  - file_path:文件路径
  - jq_schema:jq解析语法，必填,.[]表示从根结构下获取数组，.name表示从根结构下获取name字段，.[].name表示取数组内每个字典json对象的name字段
  - text_content：抽取到的是否是自读穿，默认True
  - json_lines:是否是JsonLines文件，默认False
  ```py
    from langchain_community.document_loaders import JSONLoader
    loader = JSONLoader(
        file_path = './data.json',
        jq_schema = ".[].name.age",
        text_content=False
    )
    document = loader.load()
    print(document)
  ```
  ### 5.5 TextLoader
  > 读取文本文件，比如.txt，将全部
  - RecursiveCharacterTextSplitter,递归字符文本分割器，主要用于**按照自然段落分割大文档**。是LangChain推荐的默认字符分割器。
  ```py
  from langchain_community.document_loaders import TextLoader
  from langchain_text_splitters import RecursiveCharacterTextSplitter
  loader = TextLoader("./data/test.txt",encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
      chunk_size=500,#分段的最大字符数
      chunk_overlap=50,#分段之间允许重叠字符数
      separators=["\n\n","\n","。","!"]
    )
    split_docs = splitter.split_documents(docs)
    for doc in split_docs:
      print("="*20)
      print(doc)
      print("="*20)
  ```
  ### 5.6 PyPDFLoader
  > 先下载PyPDFLoader的依赖Pypdf,pip install pypdf
  - file_path
  - mode:模式：single模式：不管有多少页都只返回一个document对象，page模式：每个页面都形成一个Document文档对象
  ```py
    loader = PyPDFLoader(
      file_path="./data/pdf1.pdf"
    )
    i = 0
    for doc in loader.lazy_load():
      i++
  ```
## LangSmith

# 1.神经网络原理
# 2.词向量
# 3.Transformer
# 4.大模型应用：
  ### 模糊问题处理
  ### 复杂模式识别
  ### 确定性逻辑处理
  ### 精确控制和高可靠性
# 5.大模型服务：
  ### deepseek
  ### 阿里云百炼
  ### ollama
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
