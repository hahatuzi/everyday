from openai import OpenAI

client = OpenAI(
    base_url="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key="sk-XXX",
)
messages = [
    {"role":"system", "content":"A公司有3个部门，市场部28人，技术部比市场部多14人，行政部人数是技术部的一半。三个部门一共多少人？请生成3条独立的推理路径，分别计算得到结果，之后对比三条路径的结果，选出最可靠的最终答案。"}
]
response = client.chat.completions.create(
    model="qwen3.8-27b",
    messages= messages
)
print(response.choices[0].message.content)