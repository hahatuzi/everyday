from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

parser = StrOutputParser()
prompt = PromptTemplate.from_template("我的邻居姓{lastname},刚生了个{gender},帮忙起个名字吧")

model = ChatTongyi(model="qwen-max",api_key="")

chain = prompt | model | parser | model
res = chain.invoke({"lastname":"王","gender":"女儿"})

print(res.content)