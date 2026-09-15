import os
from asyncio import __main__

from griffe._internal.agents.nodes import parameters
from openai import OpenAI

client = OpenAI(
    api_key= 'sk-xx',
    base_url="https://api.deepseek.com"
)
def get_ball(name:str):
    data = [
        {"name":'篮球',"numbers":5}
    ]
    res = []
    for item in data:
        if(name == item['name']):
            res.append(item)
    return res
tools=[{
  "type":"function",
    "function":{
        "name":"get_ball",
        "parameters":{
            "type":"object",
            "properties":{
                "name":{"type":"string"},
            },
            "additionalProperties":False
        },
        "strict":True
    }
}]
system_prompt = ''
message_history = []
message_history.append({"role":"system","content":system_prompt})

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

def agent(query):
  max_turns = 5
  current_turn = 1
  next_message = {"role":"user","content":query}
  while current_turn <= max_turns:
      message = get_completion(next_message)
      print(message['content'])
      if(message['tool_calls']):
          func_call_id = message['tool_calls'][0]
          func_fwargs = message['tool_calls'][1]
          func_result = get_ball(**func_fwargs)
          print(f"观察：{func_result}")
          next_message = {"role":"user","tool_call_id":func_call_id,"content":str(func_result)}
      else:
          break

if __name__ == "__main__":
    query = '篮球比赛的球员人数乘以排球比赛的球员人数，结果是多少'
    agent(query)