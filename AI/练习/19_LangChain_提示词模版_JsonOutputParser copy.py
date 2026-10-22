from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

first_prompt = PromptTemplate.from_template("我的邻居姓{lastname},刚生了个{gender},帮忙起个名字吧，要求名字为单字，并封装为json格式返回给我，要求key是name,value是你起的名字，请严格遵守该规则")
# AIMessage("{"name":"XXX"}")
second_prompt = PromptTemplate.from_template("姓名:{name},请帮我解析含义")

model = ChatTongyi(model="qwen-max",api_key="sk-")

chain = first_prompt | model | json_parser | second_prompt | model | str_parser
res = chain.invoke({"lastname":"王","gender":"女儿"})

print(res)
print(type(res))