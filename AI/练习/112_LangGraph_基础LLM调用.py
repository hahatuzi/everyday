from typing import TypedDict, Literal
from langgraph.graph import StateGraph
from langgraph.constants import START,END
from IPython.display import display,Image
from langgraph.types import Command

# 创建State
model = init_chat_model(
    model="",
    extra_body = {"thinking":{"type":"disabled"}}
)
# 2.创建state
class LLMState(TypedDict):
    user_message:str
    ai_message:str
# 3.创建Node
def llm_node(state:LLMState):
    user_message = state.get("user_message", "hi")
    response = model.invoke(user_message)
    return {"ai_message": response.text}



builder = StateGraph(LLMState)

builder.add_node("llm", llm_node)

builder.add_edge(START, "llm")
builder.add_edge('llm', END)

graph = builder.compile()
display(Image(graph.get_graph(xray = True).draw_mermaid_png()))
result = graph.invoke({})
print(result)