import requests
import time
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 模型与API密钥配置
#大模型配置(支持 DeepSeek/通义千问/兼容OpenAI接口的国产模型)
LLM_API_KEY ="sk-XXX”
LLM_API_BASE ="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1" #模型接口地址
MODEL_NAME = "deepseek-v4-pro"

#第三方实时数据API密钥(自行去对应平台中请免费密钥)
WEATHER_KEY ="你的和风天气KEY"
EXCHANGE_KEY ="你的汇率API KEY"
#初始化大模型，开启Function Ca11能力
llm = ChatOpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_API_BASE,
    model=MODEL_NAME,
    temperature=0.1,
    #低温度保证意图识别、工具调用精准
    timeout=15
)

# 2.封装三大实时查询工具(Function Cal1核心)
# 工具1:实时天气查询(对接和风天气API)
"""
    实时天气查询工具
    :paramcity:城市名称，例如:北京、上海、广州
    使用场景:用户询问某城市天气、温度、风向、体感温度、天气状况时调用
    :return:城市实时天气信息
"""
@tool
def get_real_weather(city: str) -> str:
    url = f"https://devapi.qweather.com/v7/weather/now?location={city}&key={WEATHER_KEY}'
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "200":
          return f"查询失败:{data.get('updateTime','未知错误')}"
        now = data["now"]
        return (
            f"城市:{city}\n"
            f"天状况:{now['text']}\n"
            f"温度:{now['temp']}C\n"
            f"体感温度:{now['feelsLike']}C\n"
            f"风问风力:{now['windDir']} {now['windScale']}级"
        )
    except Exception as e:
        return f"天气接口请求异常:{str(e)}"
# 工具2:实时汇率查询(对接公开汇率API)
"""
实时汇率查询工具
使用场景:用户询问货币汇率、币种换算时调用
:param base_currency:基准货币代码，大写英文，例:CNY、USD、EUR
:param target_currency:目标货币代码，大写英文，例:USD、JPY、HKD
:return:实时汇率结果
"""
@tool
def get_exchange_rate(base_currency: str, target_currency: str) -> str:
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/{base_currency}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") != "success"
            return "汇率查询失败"
        rate = data["conversion_rates"].get(target_currency)
        if not rate:
            return f"不支持该币种:{target_currency}"
        return f"1 {base_currency} = {rate} {target_currency}"
    except Exception as e:
        return f"汇率接口请求异常:{str(e)}"
# 工具3:热点新闻查询(简易公开新闻接口)
"""
热点新闻查询工具
使用场景:用户询问今日新闻、热点资讯、头条新闻时调用
:return:最新热点新闻列表
"""
@tool
def  get_hot_news() -> str:
    url = "https://api.03c3.com/toutiao/api.php"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        news_list = resp.json()[:5]  # 只取前5条
        res = "今日热点新闻:\n"
        for idx, news in enumerate(news_list, 1):
            res += f"{idx}. {news['title']}n"
        return res
    except Exception as e:
        return f"新闻接口请求异常:{str(e)}"

#注册所有工具
tools = [get_real_weather, get_exchange_rate, get_hot_news]
# 构建Agent调度器(自动路由工具调用)
prompt = ChatPromptTemplate.from_messages([
    ("system","""
    你是智能实时问答助手，可以调用工具获取外部实时数据。
    规则:
    1.问天气→调用天气工具;问汇率/货币换算→调用汇率工具;问新闻/热点→调用新闻工具
    2.工具返回原始数据后，用通顺中文整理回答，不要直接返回原始JSON
    3.非实时类问题，直接正常回答，不调用工具
    4.接口报错时如实告知用户查询失败
    """),
    MessagesPlaceholder("chat_history", optional=True),
    ("user","{input}"),
    MessagesPlaceholder("agent_scratchpad")
])

# 创建Agent&执行器
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    #开启日志，查看工具调用过程
    verbose=True,
    handle_parsing_errors=True
)
# 交互测试入门
if __name__ == "main":
    print("===实时信息问答系统(天气/汇率/新闻)启动 =====")
    print("支持提问示例:\n1.北京今天天气怎么样\n2.人民币兑美元汇率\n3.今日热点新闻\n")
    while True:
        user_q=input("请输入问题(输入exit退出):")
        if user_q.lower() == "exit":
            break
        start = time.time()
        result = agent_executor.invoke({"input": user_q})
        print(f"\n[最终回答]:{result['output']}")
        print(f"时:{time.time() - start:.2f}s\n")