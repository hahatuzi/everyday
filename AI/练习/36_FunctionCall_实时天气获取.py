from openai import OpenAI
import json

client = OpenAI()

# ---------------------- 1、定义实际工具函数（模拟实现） ----------------------
def get_weather(city: str):
    """模拟查询天气API"""
    mock_data = {
        "北京": {"temperature": "26℃", "condition": "晴"},
        "上海": {"temperature": "28℃", "condition": "多云"},
        "广州": {"temperature": "32℃", "condition": "小雨"}
    }
    res = mock_data.get(city, {"temperature": "未知", "condition": "无数据"})
    return {"city": city, **res}


def query_database(sql: str):
    """模拟数据库查询，接收SQL语句，返回查询结果"""
    # 实际项目：这里执行真实数据库cursor查询，注意SQL注入风险
    print(f"[执行SQL] {sql}")
    if "select * from user" in sql.lower():
        return [{"id":1, "name":"张三"}, {"id":2, "name":"李四"}]
    elif "count" in sql.lower():
        return [{"total": 128}]
    else:
        return {"msg": "模拟返回空结果"}


# 工具映射：工具名字 -> 本地函数
tool_map = {
    "get_weather": get_weather,
    "query_database": query_database
}

# ---------------------- 2、tools schema 描述给大模型 ----------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据城市名称查询实时天气，用户问某地天气时调用",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {"type": "string", "description": "城市名称，例如：北京、上海"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "执行SQL查询业务数据库，用户需要统计、查询业务数据时调用。只执行SELECT只读语句",
            "parameters": {
                "type": "object",
                "required": ["sql"],
                "properties": {
                    "sql": {"type": "string", "description": "SELECT查询SQL语句，禁止写修改删除语句"}
                }
            }
        }
    }
]


def chat_with_tools(user_query: str):
    messages = [
        {"role": "user", "content": user_query}
    ]

    # 第一轮：大模型判断是否要调用工具
    resp = client.chat.completions.create(
        model="gpt‑3.5‑turbo‑1106",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    msg = resp.choices[0].message

    # 👉 如果需要调用工具
    if msg.tool_calls:
        messages.append(msg)  # 把模型的tool_call消息加入会话

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"\n模型准备调用工具：{func_name}, 参数：{args}")

            # 本地执行函数
            func = tool_map[func_name]
            tool_result = func(**args)

            # 将工具返回结果塞入messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False)
            })

        # 第二轮：把工具结果丢给大模型，生成自然语言最终回答
        final_resp = client.chat.completions.create(
            model="gpt‑3.5‑turbo‑1106",
            messages=messages
        )
        return final_resp.choices[0].message.content
    else:
        # 不需要工具，直接返回回答
        return msg.content


if __name__ == "__main__":
    print(chat_with_tools("上海今天天气怎么样？"))
    print("-"*50)
    print(chat_with_tools("帮我查询user表一共有多少用户"))
