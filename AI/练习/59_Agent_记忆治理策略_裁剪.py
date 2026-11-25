from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from  langgraph.checkpoint.memory import InMemorySaver
from rich import print as rprint

# 创建内存级别的记忆存储
checkpointer = InMemorySaver()

def trim_messages(state:AgentState, runtime:Runtime) -> dict[str,any] | None:
  messages = state['messages']
  if len(messages) <= 3:
    return None
  first_message = messages[0]
  recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4]

  new_messages = [first_message] + recent_messages

  return {
    "messages":[
      RemoveMessage(id = REMOVE_ALL_MESSAGES),
      *new_messages
    ]
  }

agent = create_agent(
    model=model,
    tools = [],
    middleware = [trim_messages],
    checkpoint = checkpointer, # 让agent具备存储能力
)
# 同一个thread_id共享记忆
config = {
    "configurable":{
        "thread_id":"1"
    }
}
print("\n第一轮对话：")
response1 = agent.invoke({
    "messages":[HumanMessage("我叫张三")]},
    config=config
)
print(f"Agent:{response1['messages'][-1].content}")
response2 = agent.invoke({
    "messages":[HumanMessage("我叫什么？")]},
    config=config
)
print(f"Agent:{response2['messages'][-1].content}")


thread1_state = agent.get_state(config)
rprint(thread1_state)

response3 = agent.invoke({
    "messages":[HumanMessage("我刚才问了什么问题？")]},
    config=config
)
print(f"Agent:{response3['messages'][-1].content}")

thread2_state = agent.get_state(config)
rprint(thread2_state)