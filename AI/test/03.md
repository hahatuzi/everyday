import httpx
def get_weather(latitude,longitude):
    res = httpx.get('')
    data = res.json()
    return data
from openai import OpenAI
import json
client = OpenAI()

# 使用变量存储历史记录
message_history = []

tools = [
    {
        'type': 'function',
        "function":{
            "name":"get_weather",
            "description":"根据经纬度获取当地温度",
            "parameters":{
                "type":"object",
                "properties":{
                    "latitude":{  "type":"number"},
                    "longitude": {"type": "number"},
                },
                "required":["latitude","longitude"],
                "additionalProperties":False
            },
            "strict":True
        }
    }
]
# 给大模型发送消息，并自动保存历史记录
def get_completion(message):
    message_history.append(message)
    response = client.chat.completions.create(
        model='deepseek-v4-pro',
        messages=message_history,
        tools=tools
    )
    response_dict = dict(response.choices[0].message)
    message_history.append(response_dict)
    return response_dict

message = get_completion({"role":'user',"content":"今天北京天气如何"})
# LLM返回工具调用结果信息
print(message)

func_call_id = message['tool_calls'][0].id

func_kwargs = json.loads(message['tool_calls'][0].function.arguments)
func_result = get_weather(**func_kwargs)

# 调用函数
message = get_completion({"role":"tool","tool_call_id":func_call_id,"content":str(func_result)})
print(message)