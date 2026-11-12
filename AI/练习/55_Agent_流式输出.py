from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi

from langchain.agents import  create_agent

from langchain_community.chat_models import ChatTongyi

@tool(parse_docstring=True)
def search_customer_database(query:str) -> str:
  """
  在客户数据库中搜索信息
  Args:
    query(str):客户查询字符串，例如“张三”或者“李四”
  Returns:
    str: 客户记录字符串，包含客户姓名，登记，最近购买日期，和累计消费
  """
  if"张三" in query.lower():
    return "客户记录：张三，VIP客户，最近购买日期：2026-01-05，累计消费：￥1500"
  else :
    return f"关于客户{query},无记录"
class ContactInfo(BaseModel):
  """用户的信息"""
  name:str = Field(description = "用户姓名")
  email:str = Field(description = "用户邮箱")
  phone:str = Field(description = "用户电话")

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key="sk-"),
    system_prompt = SystemMessage(content="请分析客户的情况：1.先搜索客户数据库了解最新情况。2.如果是VIP客户，则发送感谢邮件。3.基于搜索结果生成结构化分析报告。4.如果用户提问与客户记录无关或者找不到客户信息，则返回空对象，不发送感谢邮件。")
    tools = [search_custom_data]
    response_format = ToolStrategy(schema = ContactInfo)
)

res = agent.stream({"messages":[HumanMessage(content="请分析客户张三")]},stream_mode = 'values')
for chunk in res:
  print(chunk)
print("*****************\n",res)