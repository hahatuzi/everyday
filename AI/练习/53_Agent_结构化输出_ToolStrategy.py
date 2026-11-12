from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi

from langchain.agents import  create_agent

from langchain_community.chat_models import ChatTongyi

class ContactInfo(BaseModel):
  """用户的信息"""
  name:str = Field(description = "用户姓名")
  email:str = Field(description = "用户邮箱")
  phone:str = Field(description = "用户电话")

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key="sk-"),
    response_format = ToolStrategy(schema = ContactInfo)
)

res = agent.invoke({"messages":[HumanMessage(content="从这段话中抽取结构化信息，小明的邮箱是XXX@qq.com,电话是13011112222")]})
print("*****************\n",res)