from typing import TypeDict
# __start__ → greet → uppercase → __end__

# 1.State：定义共享数据结构
class SimpleState(TypeDict):
  name:str
  greeting:str

# 2.Node:定义处理逻辑
def greet_node(state:SimpleState)：
  return {"greeting": f"Hello,{state['name']}!"}

def uppercase_node(state: SimpleState):
  return {"greeting": state['greeting'].upper()}

# 3. 创建Graph
graph_builder = StateGraph(SimpleState)
# 添加节点
graph_builder.add_node("greet", greet_node)
graph_builder.add_node("uppercase", uppercase_node)

# 添加边
graph_builder.add_edge(START, "greet")
graph_builder.add_edge("greet", "uppercase")
graph_builder.add_edge("uppercase", END)
# 编译
graph = graph_builder.compile()

display(Image(graph.get_graph(xray = True).draw_mermaid_png()))