"""
多功能智能助手，支持：
1.天气查询:查询城市天气
2.数学运算：复杂数学运算
3.时间查询：获取当前时间，日期计算
4.货币转换，多种货币之间的转换
5.信息搜索：搜索产品，新闻等信息
"""
import math
from datetime import datetime

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="获取城市天气")
def get_weather(city:str) -> str:
    """
    获取城市天气
    :param city: 城市名称
    :return:城市天气或者无数据
    """
    weather_db = {
        "北京":"多云，10-15℃，空气质量差，湿度20%",
        "上海": "晴，15-20℃，空气质量良，湿度30%",
        "深圳": "晴，20-25℃，空气质量优，湿度35%",
    }
    result = weather_db.get(city)
    if result:
        return f"{city}:{result}"
    else:
        return "未查询到结果"

@tool(description="复杂数学运算")
def calculetor(expression: str) -> str:
    """
    复杂数学运算
    :param expression: 数学表达式，可以包含：基本运算，幂运算，函数
    :return: 计算结果或者错误信息
    """
    try:
        safe_functions = {
            'sqrt': math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
        }
        result = eval(expression, {"__builtins__": {}}, safe_functions)
        return f"{expression}={result}"
    except Exception as e:
        return f"计算出错：{str(e)}\n提示：请检查表达式格式"

@tool(description="获取当前时间，日期计算")
def get_time_info(query_type:str = "current") -> str:
    """
    获取当前时间，日期计算
    :param query_type:
    :return:
    """
    now = datetime.now()
    if query_type == "current":
        return now.strftime("当前时间：%Y-%m-%d %H:%M:%S")
    elif query_type == "date":
        return now.strftime("今天是：%Y-%m-%d")
    elif query_type == "weekday":
        weekdays = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
        return f"今天是：{weekdays[now.weekday()]}"
    else:
        return f"不支持的查询类型{query_type}"

@tool(description="搜索产品，新闻等信息")
def search_info(keyword:str,category:str ="all") -> str:
    """
    搜索产品，新闻等信息
    :param keyword:
    :param category:
    :return: 搜索结果
    """
    products = {
        "手机":"iphone18(13999),小米18(7999),华为mate80(8999)",
        "耳机": "Airpods(3999),sony(2999),华为(1999)",
    }
    news = {
        "AI":"GPT5即将发布",
        "科技":"新能源汽车销量创新高"
    }
    results = []
    if category in ['product',"all"]:
        for key, value in products.items():
            if key in keyword:
                results.append(f"【产品】{key}:{value}")
    if category in ['news',"all"]:
        for key, value in news.items():
            if key in keyword or keyword in value:
                results.append(f"【新闻】{key}:{value}")
    if results:
        return "\n".join(results)
    else:
        return f"未找到关于’{keyword}‘的{category}信息"


class SmartAssistant:
    def __init__(self):
        self.model = "qwen-max"
        self.key = "sk-ws-XX"
        self.tools = [get_weather, calculetor, get_time_info, search_info]
        system_prompt = """你是一个多功能智能助手,可以帮助用户：
        ☀️ 查询天气：使用 get_weather 工具
        🧮 数学计算：使用 calculetor 工具
        ⌚️ 时间查询：使用 get_time_info 工具
        🔍 信息搜索：使用 search_info 工具
        
        重要提示：
        1.仔仔细阅读用户问题，确定需要使用哪个工具
        2.如果需要多个工具，按顺序调用
        3.总是用友好、专业的语气回答
        4.如果工具返回了数据，要用通俗易懂的语言解释给用户
        5.如果无法完成任务，诚实地告诉用户原因
        
        请始终使用中文回答。"""
        self.agent = create_agent(
            model= ChatTongyi(model = self.model,api_key=self.key),
            tools= self.tools,
            system_prompt=system_prompt
        )
        # 对话历史
        self.messages = []

    def chat(self, user_input:str)->str:
        """
        对话接口
        :param user_input:
        :return:
        """
        # 添加用户消息
        self.messages.append({"role":"user","content":user_input})
        # 调用agent
        result = self.agent.invoke({"messages":self.messages})
        # 更新消息历史
        self.messages = result["messages"]
        # 返回最后一条AI消息
        for msg in reversed(self.messages):
            if msg.type == 'ai' and msg.content:
                return msg.content
        return "抱歉，我无法处理这个请求"


    def reset(self):
        """重置对话历史"""
        self.messages = []

def main():
    assistant = SmartAssistant()
    print("="*40)
    print("🤖 多功能智能助手1.0")
    print("="*40)
    print("我可以帮助你：")
    print("☀️ 查询天气")
    print("🧮 数学计算")
    print("⌚️ 时间查询")
    print("🔍 信息搜索")
    print("\n输入'quit'退出，输入'reset' 重置对话\n")
    demos = [
        "上海今天天气怎么样？",
        "帮我算一下(25+17)*3",
        "现在几点了？",
        "告诉我最新的科技消息"
    ]
    for demo in demos:
        print(f"👤 {demo}")
        response = assistant.chat(demo)
        print(f"🤖 {response}\n")
    #     重置对话
    assistant.reset()
    print("="*40)
if __name__ == "__main__":
    main()