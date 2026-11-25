from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from  langgraph.checkpoint.memory import InMemorySaver
from rich import print as rprint
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
# ================
# 基于store
store = InMemoryStore()
namespace1 = ('users',"Bob","memories")
key1 = "preferences"
value1 = {
    "course":"数字电路与模拟电路",
    "sports":"跑步",
    "food":"奶皮子糖葫芦"
}
namespace2 = ('users',"Black","memories")
key2 = "preferences"
value2 = {
    "course":"数字电路与模拟电路",
    "sports":"跑步",
    "food":"奶皮子糖葫芦"
}

store.put(namespace1, key1, value1)
store.put(namespace2, key2, value2)
for item in store.search(("users", ),filter={"sports":"跑步"}):
  print(item)