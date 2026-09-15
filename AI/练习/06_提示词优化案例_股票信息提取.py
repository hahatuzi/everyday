import json

from openai import OpenAI
client = OpenAI(
    base_url="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key="sk-XXX",
)
schema = ['日期','股票名称','开盘价','收盘价','成交量']

example_data = [
    {
    "content":"2023-01-10，股市震荡。股票强大科技A股今日开盘价100人民币，一度飙升至105人民币，随后回落至98人民币，最终以102人民币收盘，成交量达到520000",
     "answers":{
         "日期":"2023-01-10",
         "股票名称":"强大科技A股",
         "开盘价":"100人民币",
         "收盘价": "102人民币",
         "成交量": "520000",
     }
    },
{
        "content":"2024-05-16，股市利好。股票英伟达美股今日开盘价105美元，一度飙升至109美元，随后回落至100美元，最终以116美元收盘，成交量达到350000。",
     "answers":{
         "日期":"2024-05-16",
         "股票名称":"英伟达",
         "开盘价":"105美元",
         "收盘价": "116美元",
         "成交量": "350000",
     }
    },

]
questions = [
    "2025-06-16，股市利。股票传智教育A股今日开盘价66人民币，一度飙升至70人民币，随后回落至65人民币，最终以68人民币收盘，成交量达到123000.",
    "2025-06-06，股市利好。股票黑马程序员A股今日开盘价200人民币，一度飙升至211人民币，随后回落至201人民币，最终以206人民币收盘"
]

messages = [
    {"role":"system", "content":f"你帮执完成信息性取，我给你句子，你抽取{schema}信息，按JS0N字符串输出，如果某些信息不存在，用'原文未提及'表示，请参考如下示例:"}
]

for example in example_data:
    messages.append({"role":"user", "content":example['content']})
    messages.append({"role":"assistant", "content": json.dumps(example['answers'], ensure_ascii=False)})
# for item in messages:
#     print(item)
# 向模型提问
for q in questions:
    response = client.chat.completions.create(
        model="qwen3-max",
        messages= messages + [{"role":"user", "content":f"按照实例，提取这段文字的信息：{q}"}]
    )
    print(response.choices[0].message.content)