from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import retriever
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models.tongyi import ChatTongyi

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt


model = ChatTongyi(model="qwen-max",api_key="sk-")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题，参考资料：{context}."),
        ("user","用户提问：{input}")
    ]
)
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(dashscope_api_key = 'sk-', model="text-embedding-v4"))

vector_store.add_texts(["减肥就是少吃多练","跑步是很好的运动哦","游泳的减肥效果也不错哦"])

input_text = "怎么减肥？"
# 检索知识库
result = vector_store.similarity_search(input_text,2)
reference_text ="["
for doc in result:
    reference_text += doc.page_content
reference_text += "]"

chain = prompt | print_prompt | model |StrOutputParser()

res = chain.invoke(input_text)
print(res)