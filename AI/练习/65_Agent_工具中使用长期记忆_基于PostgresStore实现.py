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

DB_URL =''
with PostgresStore.from_conn_string(DB_URL) as store:
  store.setup()
  agent = create_agent()

  response1 = agent.invoke({
    "messages":[HumanMessage('你是谁')],
    "user_id":"user_1"
  })
  print(response1)
  response2 = agent.invoke({
      "messages":[HumanMessage('你可以帮我做点什么')],
      "user_id":"user_1"
    })
    print(response2)