from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from  langgraph.checkpoint.memory import InMemorySaver
from rich import print as rprint
from langgraph.store.memory import InMemoryStore
from langgraph.store.postgres import PostgresStore
# ================
# 基于store
# store = InMemoryStore()
# namespace = ('users',)
# user_id = "user-1"
# user_name = "小明"
#
# store.put(namespace, user_id, {"name": user_name})
# item = store.get(namespace, user_id)
# print(item)
# ================
# 基于postgresStore
DB_URL = "XXX"
with PostgresStore.from_conn_string(DB_URL) as store:
    store.setup()

    namespace = ('users',)
    user_id = "user-1"
    user_name = "小明"

    store.put(namespace, user_id, {"name": user_name})
    item = store.get(namespace, user_id)
    print(item)