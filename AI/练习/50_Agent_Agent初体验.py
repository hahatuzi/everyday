from langchain.agents import create_agent
from langchian_community.chat_models.tongyi import ChatTongyi


def get_weather()->str:
  return "晴天"

agent = create_agent(
  model=ChatTongyi(model="qwen3max"),
  tools=[get_weather],
  system_prompt="你是一个聊天助手，可以回答用户问题"
)

res = agent.invoke(
  {
    "messages":[
      {"role":"user","content":"明天的天气如何"}
    ]
  }
)
print(res)
for msg in res["messages"]:
  print(type(msg).__name__, msg.content)
# HumanMessage 
# AIMessage
# ToolMessage
