from json import tool

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models import ChatTongyi


@tool(description="查询天气,传入城市名称字符串，返回字符串天气信息")
def get_weather(city:str) -> str:
    return f"{city}天气：晴天"

@before_agent
def log_before_agent(state:AgentState, runtime:Runtime) -> None:
    print(f"[before_agent{len(state['messages'])}")

@after_agent
def log_after_agent(state:AgentState, runtime:Runtime) -> None:
    print(f"[after_agent{len(state['messages'])}")
@before_model
def log_before_model(state:AgentState, runtime:Runtime) -> None:
    print(f"[before_model{len(state['messages'])}")
@after_model
def log_after_model(state:AgentState, runtime:Runtime) -> None:
    print(f"[after_model{len(state['messages'])}")
@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用了")
    return handler(request)
@wrap_tool_call
def tool_call_hook(request, handler):
    print(f"工具执行:{request.tool_call['name']}")
    return handler(request)

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key="sk-"),
    tools=[get_weather],
    middleware=[log_before_agent, log_after_agent,log_before_model,log_after_model, model_call_hook, tool_call_hook]
)

res = agent.invoke({"messages":[{"role":"user","content":"上海今天的天气怎么样？如何穿衣服？"}]})
print("*****************\n",res)