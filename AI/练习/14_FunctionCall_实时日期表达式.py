import datetime
import json
from google.protobuf import descriptor
from openai import OpenAI

client = OpenAI(
    base_url="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key="sk-1XXX",
)
# 本地工具函数，时间、日期查询
"""
后去当前时间，日期，星期
:param query_type:查询类型，可选值：date(日期),time(时间),week(星期),all(全部)
:retrun:格式化后的时间文本
"""
def getTime (query_type):
  now = datetime.datetime.now()
  week_map = {0:'星期一',1:'星期二',2:'星期三',3:'星期四',4:'星期五',5:'星期六',6:'星期七'}
  if query_type == 'date':
      return f'当前日期：{now.strftime("%Y-%m-%d")}'
  elif query_type == 'time':
      return f'当前时间：{now.strftime("%H:%M:%S")}'
  elif query_type == 'week':
      return f'今天是：{week_map[now.weekday()]}'
  elif query_type == 'all':
      return f'当前日期：{now.strftime("%Y-%m-%d")} {now.strftime("%H:%M:%S")},{week_map[now.weekday()]}'
  else:
      return '不支持的查询类型'

# 函数明细表
function_map = {
    'get_datetime':getTime,
}
# 工具描述Schema
tools = [
    {
        "type":"function",
        "function":{
            "name":"get_datetime",
            "description":"当前用户查询当前日期，时间的工具",
            "parameters":{
                "type":"Object",
                "properties":{
                    "query_type":{
                        "type":"string",
                        "description":"查询类型：date=日期,time=时间,week=星期,all=全部信息",
                        "enum":["date","time","week","all"]
                    }
                },
                "required":["query_type"]
            }
        }
    }
]
def chat_with_tools(user_input):
    messages = [{"role":"user","content":user_input}]
    resp = client.chat.completions.create(
        model = 'qwen3.8-max',
        messages = messages,
        tools = tools,
        tool_choice='auto'
    )
    resp_msg = resp.choices[0].message
    # 判断是否触发函数调用
    if resp_msg.tool_calls:
        print("【检测到函数调用】")
        for tool_call in resp_msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f'调用函数,{func_name}，入参：{args}')
            # 本地执行工具函数
            func = function_map[func_name]
            tool_result = func(**args)
            print(f'工具返回结果：{tool_result}\n')
#             追加对话上下文，模型调用记录 * 工具执行结果
            messages.append(resp_msg)
            messages.append({
                "role":"tool",
                "content":tool_result,
                "tool_call_id":tool_call.id
            })
#             第二轮：把工具结果回传给模型，生成最终回答
        final_resp = client.chat.completions.create(model = "qwen3.8-max", messages = messages)
        print('【模型最终回复】')
        print(f'{user_input}\n{final_resp.choices[0].message.content}')
    else:
        print('【无需调用工具】')
        print(resp_msg.content)


if __name__ == '__main__':
    chat_with_tools('现在几点了:')
    print('-'* 60)
    chat_with_tools('今天是几月几号：')
    print('-'* 60)
    chat_with_tools('今天是星期几：')
    print('-'* 60)
    chat_with_tools('请告诉我现在完整的日期，时间，和星期:')
    print('-'* 60)
    chat_with_tools('你好呀')
    print('-'* 60)