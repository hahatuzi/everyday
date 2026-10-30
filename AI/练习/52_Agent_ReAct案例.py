from json import tool

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

from FewShot提示词模版 import model

@tool(description="获取股票价格")
def get_price(name:str) -> str:
    return f"股票{name}的价格是20元"
@tool(description="获取股票信息")
def get_info(name:str) -> str:
    return f"股票{name},是一家A股上市公司，专注于某某领域"

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key="sk-"),
    tools = [get_price, get_info],
    system_prompt = """你是严格遵循ReAct框架的智能体，必须按「思考-行动-观察-再思考」的流程解决问题,且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我"""
)

for chunk in agent.stream(
    {"messages":[{"role":"user", "content":"东方财富的股价多少，并介绍一下它"}]},
    stream_mode="values"
):
   latest_message = chunk["messages"][-1]
   if latest_message.content:
       print(latest_message.content)
try:
    if latest_message.tool_calls:
        print(f"Calling tools:{[tc['name'] for tc in latest_message.tool_calls]}")
except AttributeError as e:
    pass