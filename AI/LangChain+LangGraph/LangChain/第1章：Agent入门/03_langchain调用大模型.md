# 一：langchain调用大模型
### 1.1 langchain调用千问模型
```py
from langchian_community.llms.tongyi import Tongyi
llm = Tongyi(model = 'qwen-max')
res = llm.invoke('帮我做个作业吧')
```

### 1.2 langchain调用本地大模型
```py
  from langchain_ollama import OllamaLLM

  model = OllamaLLM(model="qwen3:4b")

  res = model.invoke(input = '你是谁？')
  print(res)
```
### 1.3 langchain调用嵌入大模型
### 1.4 langchain的流式输出
- model.invoke：一次性输出
- model.stream:流式输出
```py
  from langchain_ollama import OllamaLLM

  model = OllamaLLM(model="qwen3:4b")

  res = model.stream(input = '你是谁？')
  for chunk in res:
    print(chunk, end="",flush=True)
    # flush为直接刷新
```
# 二、langchain调用聊天模型
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
# 三、Embedding Model文本嵌入模型
<!-- 将文本作为输入，转化为一个浮点列表向量 -->
```py
from langchain_community.embeddings import DashScopeEmbeddings
model = DashScopembeddings()
print(model.embed_query('我喜欢你'))
print(model.embed_documents(['我爱你','我喜欢你']))
```

# 四、langchain的提示词模版PromptTemplate类
> 该类用来协助优化提示词，支持变量的注入，可以构建一个自定义的基础提示词模版
### 4.1 标准写法
```py
from langchain_core.prompts import PromptTemplete
prompt_template = PromptTemplate.from_template("我的邻居叫{},刚生了个{gender},帮忙起个名字吧")
prompt_text = prompt_template.format(name='章',gender="女")
model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)
```
### 4.2 chain链式写法
```py
from langchain_core.prompts import PromptTemplete
prompt_template = PromptTemplate.from_template("我的邻居叫{},刚生了个{gender},帮忙起个名字吧")
prompt_text = prompt_template.format(name='章',gender="女")
model = Tongyi(model="qwen-max")
chain = prompt_template | model
res = chain.invoke(input=prompt_text)
```