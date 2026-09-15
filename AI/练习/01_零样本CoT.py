from openai import OpenAI

client = OpenAI(
    base_url="https://ws-omu6172u8mjmo9ut.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    api_key="sk-XXX",
)
messages = [
    {"role":"system", "content":"一个商店进货，第一批进12箱牛奶，每箱24盒。卖掉86盒之后，又补货7箱。现在店里一共有多少盒牛奶？请一步步思考，然后给出最终答案。"}
]
response = client.chat.completions.create(
    model="qwen3.8-27b",
    messages= messages
)
print(response.choices[0].message.content)

# ============添加请一步步思考，然后给出最终答案。这句话之前的结果============
# 第一批牛奶：
# 12 × 24 = 288（盒）
# 卖掉后剩下：
# 288 − 86 = 202（盒）
# 又补货7箱：
# 7 × 24 = 168（盒）
# 现在一共有：
# 202 + 168 = 370（盒）
# **答：现在店里一共有 370 盒牛奶。**

# =================之后的============
# 第一步：第一批进货的牛奶盒数
# 12 箱 × 每箱 24 盒 = 288 盒
# 第二步：卖掉 86 盒后剩下的盒数
# 288 盒 − 86 盒 = 202 盒
# 第三步：又补货 7 箱，增加的盒数
# 7 箱 × 每箱 24 盒 = 168 盒
# 第四步：现在店里一共有
# 202 盒 + 168 盒 = 370 盒
# 最终答案：**370 盒**。
