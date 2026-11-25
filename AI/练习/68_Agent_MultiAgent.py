# ========================================
# 第一步：基本配置
# ========================================
from dashscope.common.env import api_key
from langchain.agents import create_agent
from langchain_community.vectorstores.milvus import Milvus


# ========================================
# 旅行agent
# ========================================
travel_agent = create_agent(
    model = model,
    tools = tools,
    system_prompt = """你是一个旅行助手Agent。你为用户搜索到达婚礼地点的理想航班，您不能再追问任何后续问题
您必须根据以下标准找到最佳航班选择:
价格(最低，经济舱
持续时间(最短
日期(您认为在该地点举行婚礼的最佳时间)
为了使事情变得简单，只寻找一张票，单程。
你不会得到额外的信息，只有出发地和目的地。你的工作是批判性地思考最佳选择。
一旦你找到了最好的选项，让用户知道你的候选列表。
调用搜索航班工具时，如果是地点在中国，需要使用zh-cn作为Locale参数。
    """
)

response = awat travel_agent.aiinvoke()
# ========================================
# 场馆agent
# ========================================
web_search = TavilySearch(max_results = 5, topic = "general")
venue_agent = create_agent()
response = venue_agent.invoke(
  ["messages":[HumanMessage("上海有哪些适合举办婚礼的场馆，100人左右")]]
)

# ========================================
# 歌单agent
# ========================================
db = SQLDatabase.from_url("sqlite:////resources/Chinook.db")
def query_playlist_db(query:str) -> str:
  try:
    return db.run(query)
  except Exception as e:
    return f"error query database: {e}"
song_agent = create_agent()
res = song_agent.invoke(
  {
    "messages":[HumanMessage("爵士风格")]
  }
)
# ========================================
# 主agent
# ========================================
class WeddingState(AgentState):
  origin:str
  destination:str
  guest_count:str
  genre:str

@tool
def update_state(origin: str, destination: str, guest_count: str, genre: str, runtime:ToolRuntime) -> str:
  """当你询问用户，知道下列所有值时更新State:origin、destination、guest_count、genre"""
  return Command(update={
    "origin": origin,
    "destination": destination,
    "guest_count": guest_count,
    "genre": genre,
    "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]
    } 
)
@tool
async def search_flights(runtime: ToolRuntime) -> str:
  """旅行Agent搜索飞往理想婚礼地点的航班."""
  origin = runtime.state["origin"]
  destination = runtime.state["destination"]
  content = f"查询从{origin}到{destination}的航班"
  
  response = await travel_agent.ainvoke({"messages": [HumanMessage(content)]})
  return response['messages'][-1].content

@tool
def search_venues(runtime: ToolRuntime) -> str:
    """场地Agent根据给定的地点和宾客数量寻找最佳的婚礼场地."""
    destination = runtime.state["destination"]
    capacity = runtime.state["guest_count"]
    content =f"在{destination}寻找适合{capacity}宾客的婚礼场地"
    response = venue_agent.invoke({"messages": [HumanMessage(content)]})
    return response['messages'][-1].content

@tool
def suggest_playlist(runtime: ToolRuntime) -> str:
    """播放列表Agent根据类型风格策划完美的播放列表."""
    genre = runtime.state["genre"]
    content=f"策划符合{genre}风格的婚礼播放列表的曲目"
    response = playlist_agent.invoke({"messages":[HumanMessage(content)]})
    return response['messages'][-1].content


from langchain.agents import create_agent
coordinator = create_agent(
   model="deepseek-flash",
  state_schema=WeddingState,
  tools=[search_flights, search_venues, suggest_playlist, update_state],
  system_prompt="""
    你是婚礼协调员。你负责与用户沟通，找到更新状态所需的所有信息，并更新到state。
    一旦完成，你就可以委派任务了。将查找航班、搜索场地和策划播放列表的任务委派给您的专家Agent。
    当你收到他们的答案，为我设计一场完美的婚礼方案。
    """
)
response = await coordinator.ainvoke({
"messages”:[HumanMessage(content="我来自北京，我想在上海举办一场100人的婚礼，爵士风格的。")]，
})

for message in response["messages"]:
  message.pretty_print()