from openai import OpenAI
from sympy import true

client = OpenAI(
    base_url="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key="sk-XXX",
)
stream = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages= [{"role":"user", "content":"北京有什么好吃的"}],
    stream=True
)
full_text = ""
for chunk in stream:
    # 部分chunk为空，要做判断
    if chunk.choices and chunk.choices[0].delta.content:
        text = chunk.choices[0].delta.content
        full_text += text
        print(text, end="", flush=True) # 实时打印，打字机效果
print("\n\n完整结果：", full_text)