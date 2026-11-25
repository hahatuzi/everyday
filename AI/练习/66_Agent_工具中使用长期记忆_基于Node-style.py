from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

class CustomState(AgentState):
  user_id:NotRequired[str]

def save_user_info(name:str, runtime:ToolRuntime) -> str:
  namespace("users",)
  key = runtime.state["user_id"]
  value = {"name":name}

  runtime.store.put(namespace, key, value)
  return "saved"

@tool(parse)
def get_user_info(runtime:ToolRuntime) -> str:
  namespace = ("users",)
  key = runtime.state["user_id"]
  item= runtime.store.get(namespace, key)
  return str(item.value) if item else "unknown"

response = agent.invoke({
  "messages":[HumanMessage]
})