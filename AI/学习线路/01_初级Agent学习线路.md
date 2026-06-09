# 初级 AI Agent 工程师学习路线

> 适用阶段：有基本编程概念（不限语言），从零开始进入 AI Agent 领域
> 更新日期：2026年6月
> 前置条件：会用电脑、有基本的编程概念即可（如有 Python 基础可跳过阶段一）

---

## 目录

1. [能力模型总览](#一能力模型总览)
2. [阶段一：Python 速成（2-3 周）](#二阶段一python-速成)
3. [阶段二：AI 与大模型基础认知（2-3 周）](#三阶段二ai-与大模型基础认知)
4. [阶段三：LLM API 调用入门（2-3 周）](#四阶段三llm-api-调用入门)
5. [阶段四：Prompt 工程基础（2 周）](#五阶段四prompt-工程基础)
6. [阶段五：第一个 AI Agent（3-4 周）](#六阶段五第一个-ai-agent)
7. [阶段六：RAG 入门与项目实战（3-4 周）](#七阶段六rag-入门与项目实战)
8. [B站与学习资源推荐](#八b站与学习资源推荐)
9. [书单推荐](#九书单推荐)

---

## 一、能力模型总览

```
                      初级 AI Agent 工程师
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐          ┌────▼────┐
   │ 编程基础  │          │ AI 认知    │          │ Agent实战 │
   │          │          │            │          │          │
   │• Python基础语法│      │• 大模型概念   │          │• API调用    │
   │• 数据类型/函数  │      │• Token/上下文 │          │• Tool Calling│
   │• JSON/HTTP    │      │• Prompt基础   │          │• 简单Agent   │
   │• 基础调试      │      │• 模型对比     │          │• RAG入门     │
   └──────────┘          └─────────────┘        └──────────┘
```

### AI Agent 工程师三级进阶定位

| 层级 | 角色 | 核心能力 | 本文定位 |
|------|------|---------|---------|
| **初级** | Agent 使用者/入门开发者 | 能用 API 搭建简单的 Agent 应用 | **本文** |
| **中级** | Agent 开发者 | 独立构建可落地的 Agent 系统 | → 进阶 |
| **高级** | Agent 架构师 | 多 Agent 编排、企业级治理 | → 进阶 |

### 零基础 → 初级 核心转变

```
零基础                             学完后
  │                                   │
不会 Python        ──────────→   能用 Python 调用 API
不知道什么是 Agent  ──────────→   理解 Agent = LLM + 工具 + 循环
没用过 AI API      ──────────→   能调用 GPT/DeepSeek 写程序
不会写 Prompt      ──────────→   能用结构化 Prompt 控制模型输出
没做过 Agent 项目  ──────────→   有 1-2 个可运行的 Agent Demo
```

---

## 二、阶段一：Python 速成

> **周期**：2-3 周（有 Python 基础可跳过）  
> **目标**：能写基本的 Python 脚本，能调用 HTTP API

### 2.1 为什么是 Python？

- AI/ML 生态 99% 的工具和 SDK 都基于 Python
- 语法简洁，学习成本低，适合快速上手
- 社区资源最丰富，遇到问题容易找到答案

### 2.2 必学内容（只学 Agent 开发需要的）

#### 基础语法（1 周）

```python
# 1. 变量与数据类型
name = "AI Agent"          # 字符串
version = 1.0              # 浮点数
is_active = True           # 布尔值
tools = ["搜索", "计算"]    # 列表
config = {"model": "gpt-4o", "temp": 0.7}  # 字典

# 2. 条件与循环
temperature = 0.8
if temperature > 0.7:
    print("模型会很发散")
elif temperature > 0.3:
    print("平衡模式")
else:
    print("模型会很确定")

for tool in tools:
    print(f"可用工具：{tool}")

# 3. 函数定义
def call_llm(prompt: str, model: str = "gpt-4o") -> str:
    """调用大模型 API（占位函数）"""
    return f"[{model}] 回复：{prompt[:20]}..."

result = call_llm("你好", model="deepseek-chat")
```

#### 重点掌握（1 周）

```python
# 4. 字典操作（API 交互核心）
import json

# API 返回的就是 JSON → Python dict
response = '{"choices":[{"message":{"content":"你好！"}}]}'
data = json.loads(response)  # JSON 字符串 → dict
answer = data["choices"][0]["message"]["content"]
print(answer)  # 你好！

# 5. HTTP 请求（调用 API 必备）
import requests

# GET 请求
resp = requests.get("https://api.example.com/status")
print(resp.json())

# POST 请求（调用 AI API 的核心方式）
resp = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": "Bearer sk-xxx"},
    json={
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "你好"}],
    },
)
print(resp.json())

# 6. 错误处理（API 调用必备）
try:
    resp = requests.get("https://api.example.com/data", timeout=10)
    resp.raise_for_status()  # 检查 HTTP 错误
    data = resp.json()
except requests.exceptions.Timeout:
    print("请求超时！")
except requests.exceptions.RequestException as e:
    print(f"请求失败：{e}")
```

### 2.3 不需要学的

```
暂时不用学（Agent 开发暂时用不到）：
✗ 面向对象高级用法（继承、多态、元类）
✗ 多线程/异步编程（初期不需要）
✗ 数据库操作（SQLAlchemy 等）
✗ Web 框架（Flask/Django）
✗ 数据分析库（Pandas/NumPy）
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| Python 零基础全套教程 | [BV1WgVr6REPJ](https://www.bilibili.com/video/BV1WgVr6REPJ/) | 2026最新，568集全 |
| Python 速成（2小时） | [B站搜索：Python 2小时速成](https://search.bilibili.com/all?keyword=Python+2%E5%B0%8F%E6%97%B6%E9%80%9F%E6%88%90) | 有编程基础可快速过 |

---

## 三、阶段二：AI 与大模型基础认知

> **周期**：2-3 周  
> **目标**：理解大模型是什么、能做什么、有哪些主流模型

### 3.1 核心概念（必须先理解）

```
┌─────────────────────────────────────────────┐
│              AI Agent 家族关系               │
│                                              │
│  人工智能 (AI)                                │
│    └── 机器学习 (ML)                          │
│         └── 深度学习 (DL)                     │
│              └── 大语言模型 (LLM)              │
│                   └── AI Agent（本文主角）     │
│                        使用 LLM 作为"大脑"    │
│                        能调用工具、自主决策     │
└─────────────────────────────────────────────┘
```

#### 关键概念速查

| 概念 | 一句话解释 | 类比 |
|------|-----------|------|
| **LLM（大语言模型）** | 能理解和生成文本的超级 AI | 一个读过互联网所有书的"人" |
| **Token** | 模型处理文本的最小单位 | 相当于"字/词"，但不是一一对应 |
| **上下文窗口** | 模型一次能"看到"的文本上限 | 像人的短期记忆，有容量限制 |
| **Temperature** | 控制回答的随机性（0-2） | 0=照本宣科，1=天马行空 |
| **Prompt** | 发给模型的指令/问题 | 你对 AI 说的话 |
| **API** | 通过网络调用模型的方式 | 像点外卖：下单→等待→拿到结果 |

### 3.2 主流模型速览

| 模型 | 公司 | 特点 | 适合场景 |
|------|------|------|---------|
| **GPT-4o** | OpenAI | 综合最强，多模态 | 复杂推理、图片理解 |
| **Claude 4** | Anthropic | 长上下文、安全 | 长文档分析、代码生成 |
| **DeepSeek-V3** | 深度求索 | 性价比高、中文强 | 日常开发、中文场景 |
| **Gemini 2.5** | Google | 超长上下文 1M | 超长文档处理 |
| **Qwen3** | 阿里 | 开源、中文优化 | 私有化部署 |

### 3.3 Token 是什么？（必懂）

```python
# 中文：1 个汉字 ≈ 1-2 个 Token
"你好" → 2 个 Token

# 英文：1 个单词 ≈ 1-2 个 Token
"Hello World" → 2 个 Token

# 为什么要关心 Token？
# 1. API 按 Token 计费
# 2. 模型有 Token 上限（上下文窗口）
# 3. Prompt 太长会被截断

# 各模型上下文窗口对比
"""
GPT-4o:      128K tokens  ≈ 一本中篇小说
Claude 4:    200K tokens  ≈ 一本长篇小说
Gemini 2.5:  1M tokens    ≈ 《三体》三部曲
DeepSeek-V3: 128K tokens  ≈ 一本中篇小说
"""
```

### 3.4 Agent 到底是什么？

```
普通 LLM（问答机器人）:
  你问 → 它答 → 结束
  只能"说"，不能"做"

AI Agent（智能体）:
  你给任务 → 它思考 → 它调用工具 → 观察结果 → 再思考 → ... → 完成任务
  能"说"，也能"做"

核心公式：Agent = LLM（大脑） + Tools（手） + Loop（循环决策）
```

```
                    ┌──────────────────┐
                    │    AI Agent      │
                    │                  │
   用户任务 ──────→ │  ① 思考(LLM)     │
                    │  ② 决定用什么工具  │
                    │  ③ 执行工具       │
                    │  ④ 观察结果       │
                    │  ⑤ 继续思考...    │
                    │  ⑥ 返回最终答案   │────→ 完成任务
                    └──────────────────┘
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| AI Agent 是什么（35分钟精华） | [BV1dxm6YPEDB](https://www.bilibili.com/video/BV1dxm6YPEDB/) | 最透彻的 Agent 讲解 |
| 大模型基础概念科普 | [B站搜索：大模型是什么 通俗](https://search.bilibili.com/all?keyword=%E5%A4%A7%E6%A8%A1%E5%9E%8B+%E9%80%9A%E4%BF%97) | 零基础科普 |
| 菜鸟教程 AI Agent | [runoob.com/ai-agent](https://www.runoob.com/ai-agent/ai-agent-tutorial.html) | 图文教程，适合阅读 |

---

## 四、阶段三：LLM API 调用入门

> **周期**：2-3 周  
> **目标**：能用 Python 调用大模型 API，完成基本的文本生成

### 4.1 获取 API Key

```
方式一：DeepSeek（推荐入门，便宜）
  1. 访问 platform.deepseek.com
  2. 注册账号 → API Keys → 创建 Key
  3. 充值 10 元即可开始（¥1/百万 Token）

方式二：OpenAI
  1. 访问 platform.openai.com
  2. 注册 → API Keys → 创建 Key
  3. 需要海外手机号和信用卡

方式三：免费/低成本替代
  - SiliconFlow（硅基流动）：提供多种开源模型，有免费额度
  - 阿里百炼：通义千问 API，有免费额度
```

### 4.2 第一次 API 调用

```python
# 安装 openai 库（兼容 DeepSeek）
# pip install openai

from openai import OpenAI

# ========== 方式一：调用 DeepSeek（推荐）==========
client = OpenAI(
    api_key="sk-your-deepseek-key",  # 替换为你的 Key
    base_url="https://api.deepseek.com",  # DeepSeek 的地址
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "用一句话解释什么是 AI Agent"},
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)
# 输出：AI Agent 是一种能自主感知环境、做出决策并执行行动来完成任务的智能程序。

# ========== 方式二：调用 OpenAI ==========
# client = OpenAI(api_key="sk-your-openai-key")
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Hello"}],
# )
```

### 4.3 多轮对话

```python
# 多轮对话：把历史消息都带上
messages = [
    {"role": "system", "content": "你是数学老师"},
]

# 第一轮
messages.append({"role": "user", "content": "3 + 5 等于多少？"})
response = client.chat.completions.create(model="deepseek-chat", messages=messages)
answer = response.choices[0].message.content
messages.append({"role": "assistant", "content": answer})
print(f"AI: {answer}")

# 第二轮（模型记得上一轮的内容）
messages.append({"role": "user", "content": "再乘以 2 呢？"})
response = client.chat.completions.create(model="deepseek-chat", messages=messages)
answer = response.choices[0].message.content
print(f"AI: {answer}")
# 模型知道"它"指的是 8，所以回答 16
```

### 4.4 流式输出（打字机效果）

```python
# 流式：一个字一个字出来，用户体验好
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "写一首关于编程的短诗"}],
    stream=True,  # 关键参数
)

print("AI: ", end="", flush=True)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()  # 换行
```

### 4.5 角色扮演消息格式

```python
# System / User / Assistant 三者的区别
messages = [
    {
        "role": "system",
        "content": "你是一个毒舌的代码审查员，每个回复都要吐槽代码写得烂，但最后给出改进建议。"
    },
    {"role": "user", "content": "请审查这段代码：\ndef add(a,b): return a+b"},
]

# System: 设定 AI 的角色和行为（只在一开始设一次）
# User:   用户说的话
# Assistant: AI 之前回复的内容（多轮对话时需要带上）
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| DeepSeek API 调用入门 | [B站搜索：DeepSeek API 调用](https://search.bilibili.com/all?keyword=DeepSeek+API+%E8%B0%83%E7%94%A8) | 中文教程多 |
| Python 调用 LLM API | [B站搜索：Python 调用大模型API](https://search.bilibili.com/all?keyword=Python+%E8%B0%83%E7%94%A8%E5%A4%A7%E6%A8%A1%E5%9E%8BAPI) | 入门实战 |

---

## 五、阶段四：Prompt 工程基础

> **周期**：2 周  
> **目标**：学会写出高质量 Prompt，让 AI 精准输出

### 5.1 Prompt 的黄金公式

```
好的 Prompt = 角色 + 任务 + 约束 + 格式

角色：你是一个 ____
任务：请帮我 ____
约束：要求 ____ / 不要 ____
格式：输出格式为 ____
```

```python
# ❌ 糟糕的 Prompt
bad_prompt = "写个产品介绍"

# ✅ 好的 Prompt
good_prompt = """
你是一个资深产品经理。

请为以下产品写一段介绍：
产品名：AI 智能日程助手
核心功能：自动安排会议、冲突检测、智能提醒

要求：
- 字数在 100-150 字之间
- 突出"节省时间"这个卖点
- 语气专业但不生硬
- 不要使用"颠覆""革命性"等夸张词汇

输出格式：
【标题】
【一句话卖点】
【详细介绍】
"""

# 发给模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": good_prompt}],
)
print(response.choices[0].message.content)
```

### 5.2 常用 Prompt 技巧

```python
# 技巧1：Few-Shot（给示例）
few_shot = """
将用户输入分类为"正面"或"负面"。

示例1：
输入：这个产品很好用
分类：正面

示例2：
输入：客服态度太差了
分类：负面

现在请分类：
输入：{user_text}
分类：
"""

# 技巧2：Chain of Thought（让模型一步一步思考）
cot_prompt = """
问题：小明有 15 个苹果，给了小红 3 个，又买了 7 个，最后吃了 2 个，还剩几个？

请一步一步思考：
第一步：初始数量是 15
第二步：给了 3 个后，剩余 15-3=12
第三步：买了 7 个后，变成 12+7=19
第四步：吃了 2 个后，剩余 19-2=17
最终答案：17 个
"""

# 技巧3：设定输出格式
format_prompt = """
请提取以下文本中的关键信息，以 JSON 格式输出：

文本：张三，28岁，Java工程师，在北京工作

输出格式（只输出JSON，不要其他内容）：
{
  "name": "",
  "age": 0,
  "job": "",
  "city": ""
}
"""
```

### 5.3 常见的 Prompt 调优方法

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| 回答太短 | 没指定长度 | 加"至少200字"或"详细说明" |
| 回答太长 | 没限制长度 | 加"控制在100字以内" |
| 回答跑题 | 任务描述模糊 | 更具体地描述需求 |
| 格式不对 | 没指定输出格式 | 给出格式模板或示例 |
| 回答太发散 | Temperature 太高 | 降低到 0.3-0.5 |
| 回答太死板 | Temperature 太低 | 提高到 0.7-0.9 |

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| Prompt 工程入门 | [B站搜索：Prompt 工程 入门](https://search.bilibili.com/all?keyword=Prompt+%E5%B7%A5%E7%A8%8B+%E5%85%A5%E9%97%A8) | 零基础学写 Prompt |
| 结构化 Prompt 技巧 | [B站搜索：结构化Prompt 技巧](https://search.bilibili.com/all?keyword=%E7%BB%93%E6%9E%84%E5%8C%96Prompt) | 写出高质量 Prompt |

---

## 六、阶段五：第一个 AI Agent

> **周期**：3-4 周  
> **目标**：从零构建一个能调用工具的 AI Agent

### 6.1 Agent 核心循环（ReAct 模式）

```
Agent 工作流程（ReAct = Reasoning + Acting）：

1. 用户给任务："北京今天天气怎么样？"
2. Agent 思考：我需要查天气 → 决定调用 get_weather 工具
3. 执行工具：get_weather("北京") → "北京今天晴，25°C"
4. 观察结果：拿到了天气信息
5. 继续思考：信息足够了 → 生成最终回答
6. 返回："北京今天天气晴朗，气温25°C，适合户外活动！"
```

### 6.2 第一个 Agent：代码实战

```python
import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key",
    base_url="https://api.deepseek.com",
)

# ========== 第一步：定义工具 ==========
def get_weather(city: str) -> str:
    """获取城市天气（模拟）"""
    weather_data = {
        "北京": "晴，25°C，湿度40%",
        "上海": "多云，28°C，湿度65%",
        "深圳": "阵雨，30°C，湿度80%",
    }
    return weather_data.get(city, f"未找到{city}的天气信息")

def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        # 安全计算（只允许数字和基本运算符）
        allowed = set("0123456789+-*/().% ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含不允许的字符"
        result = eval(expression)
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算错误：{e}"

def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

# 工具注册表
TOOLS = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time,
}

# ========== 第二步：定义工具描述（给模型看）==========
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海、深圳"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如：'2+3*4'、'(10+5)*2'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
]

# ========== 第三步：Agent 主循环 ==========
def agent_run(user_query: str, max_steps: int = 5) -> str:
    """
    Agent 主循环：思考 → 行动 → 观察 → 重复
    """
    messages = [
        {"role": "system", "content": "你是一个智能助手，可以使用工具来回答用户问题。当需要查询信息时，请调用相应的工具。"},
        {"role": "user", "content": user_query},
    ]

    for step in range(max_steps):
        print(f"\n--- 第 {step + 1} 步 ---")

        # 调用 LLM，让它决定下一步做什么
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",  # 让模型自己决定要不要用工具
        )

        assistant_msg = response.choices[0].message

        # 如果模型不调用工具，直接返回答案
        if not assistant_msg.tool_calls:
            print(f"Agent 回答: {assistant_msg.content}")
            return assistant_msg.content

        # 处理工具调用
        messages.append(assistant_msg)

        for tool_call in assistant_msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"调用工具: {func_name}({func_args})")

            # 执行工具
            func = TOOLS.get(func_name)
            if func:
                result = func(**func_args)
            else:
                result = f"未知工具：{func_name}"

            print(f"工具返回: {result}")

            # 把工具结果加入消息历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "抱歉，处理超时，请简化问题后重试。"

# ========== 第四步：测试 Agent ==========
# 测试1：需要调用工具
agent_run("北京今天天气怎么样？适合出去玩吗？")

# 测试2：需要调用多个工具
agent_run("现在几点了？帮我算一下 156 * 23 等于多少？")

# 测试3：不需要工具
agent_run("什么是 Python？请用一句话解释。")
```

### 6.3 运行结果示例

```
用户：北京今天天气怎么样？适合出去玩吗？

--- 第 1 步 ---
调用工具: get_weather({'city': '北京'})
工具返回: 晴，25°C，湿度40%

--- 第 2 步 ---
Agent 回答: 北京今天天气晴朗，气温25°C，湿度40%，
非常舒适！非常适合户外活动，建议做好防晒哦~ ☀️
```

### 6.4 做一个有界面的 Agent（Streamlit）

```python
# pip install streamlit
# 保存为 agent_app.py，运行：streamlit run agent_app.py

import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="我的第一个 AI Agent", page_icon="🤖")
st.title("🤖 我的第一个 AI Agent")

# 侧边栏：API 配置
with st.sidebar:
    st.header("⚙️ 配置")
    api_key = st.text_input("API Key", type="password")
    model = st.selectbox("模型", ["deepseek-chat", "gpt-4o"])

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 调用 Agent
    if api_key:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                messages = [
                    {"role": "system", "content": "你是智能助手"},
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages[-10:]],  # 最近10轮
                ]

                # 流式输出
                stream = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                )
                response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.warning("请先在侧边栏输入 API Key")
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| AI Agent 从零搭建 | [BV1Z7ZwYHENT](https://www.bilibili.com/video/BV1Z7ZwYHENT/) | 手把手构建 Agent |
| Streamlit 快速入门 | [B站搜索：Streamlit 入门](https://search.bilibili.com/all?keyword=Streamlit+%E5%85%A5%E9%97%A8) | 给 Agent 加界面 |
| 从0到1搭建AI助手 | [B站搜索：从0到1搭建AI助手](https://search.bilibili.com/all?keyword=%E4%BB%8E0%E5%88%B01%E6%90%AD%E5%BB%BAAI%E5%8A%A9%E6%89%8B) | 完整项目实战 |

---

## 七、阶段六：RAG 入门与项目实战

> **周期**：3-4 周  
> **目标**：理解 RAG 概念，完成一个知识库问答项目

### 7.1 什么是 RAG？

```
RAG = Retrieval Augmented Generation（检索增强生成）

问题：LLM 的知识有截止日期，而且不知道你的私有文档

RAG 解决方案：
  1. 把你的文档切成小块
  2. 转成向量存入数据库
  3. 用户提问时，先检索相关文档片段
  4. 把文档片段 + 问题一起发给 LLM
  5. LLM 基于文档内容回答

效果：让 LLM 能回答"你的"文档里的内容！
```

```
没有 RAG：                        有 RAG：
用户问"公司年假政策？"             用户问"公司年假政策？"
     │                                  │
     ▼                                  ▼
  直接问 LLM                        1. 检索"年假"相关文档片段
     │                                  │
     ▼                                  ▼
  LLM：不知道...                   2. 找到：入职满1年享5天年假
  （没有公司内部知识）                    │
                                        ▼
                                    3. LLM + 文档片段
                                        │
                                        ▼
                                    4. 回答：入职满1年后可享受5天年假
```

### 7.2 简易 RAG 实现

```python
# pip install chromadb openai
import chromadb
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key",
    base_url="https://api.deepseek.com",
)

# ========== 第一步：准备文档 ==========
documents = [
    "公司年假政策：入职满1年的员工享有5天带薪年假，满3年享有10天，满5年享有15天。",
    "公司位于北京市海淀区中关村软件园，地铁13号线西二旗站下车步行10分钟。",
    "工作时间：周一至周五 9:00-18:00，午休12:00-13:00，弹性打卡30分钟。",
    "加班政策：工作日加班按1.5倍工资计算，周末加班按2倍计算，法定节假日按3倍计算。",
    "请假流程：需提前1天在OA系统提交申请，紧急情况可电话向直属领导请假。",
]

# ========== 第二步：创建向量数据库 ==========
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="company_docs")

# 添加文档（chromadb 会自动向量化）
for i, doc in enumerate(documents):
    collection.add(
        documents=[doc],
        ids=[f"doc_{i}"],
    )

# ========== 第三步：检索 + 生成 ==========
def ask_rag(question: str, top_k: int = 2) -> str:
    """RAG 问答：先检索相关文档，再让 LLM 基于文档回答"""

    # 1. 检索相关文档
    results = collection.query(
        query_texts=[question],
        n_results=top_k,
    )
    retrieved_docs = results["documents"][0]
    print(f"检索到 {len(retrieved_docs)} 条相关文档：")
    for doc in retrieved_docs:
        print(f"  - {doc[:50]}...")

    # 2. 构建带上下文的 Prompt
    context = "\n".join(retrieved_docs)
    prompt = f"""请根据以下公司文档回答问题。如果文档中没有相关信息，请明确说"文档中未找到相关信息"。

【公司文档】
{context}

【用户问题】
{question}

【回答】"""

    # 3. 调用 LLM 生成答案
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # RAG 场景用低温度，减少幻觉
    )
    return response.choices[0].message.content

# ========== 测试 ==========
print("\n" + "="*50)
print("问：公司的年假政策是什么？")
print("答：", ask_rag("公司的年假政策是什么？"))

print("\n" + "="*50)
print("问：公司在哪里？怎么去？")
print("答：", ask_rag("公司在哪里？怎么去？"))

print("\n" + "="*50)
print("问：公司有食堂吗？")
print("答：", ask_rag("公司有食堂吗？"))
# 预期：文档中未找到相关信息
```

### 7.3 综合项目：个人知识库助手

```
项目名称：个人知识库问答助手
周期：2 周

功能：
  1. 上传自己的文档（TXT/MD/PDF）
  2. 自动分块、向量化存储
  3. 用自然语言提问
  4. 回答带引用来源

技术栈：
  - Python + Streamlit（界面）
  - ChromaDB（向量数据库）
  - DeepSeek API（LLM）
  - PyPDF2（读取PDF）

项目文件结构：
  knowledge-agent/
  ├── app.py              # Streamlit 主程序
  ├── document_loader.py  # 文档加载与分块
  ├── vector_store.py     # 向量存储与检索
  ├── rag_engine.py       # RAG 核心逻辑
  └── requirements.txt    # 依赖
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| RAG 原理与实战 | [B站搜索：RAG 原理 实战 入门](https://search.bilibili.com/all?keyword=RAG+%E5%8E%9F%E7%90%86+%E5%AE%9E%E6%88%98+%E5%85%A5%E9%97%A8) | RAG 零基础入门 |
| 用 ChromaDB 搭建知识库 | [B站搜索：ChromaDB 知识库](https://search.bilibili.com/all?keyword=ChromaDB+%E7%9F%A5%E8%AF%86%E5%BA%93) | 向量数据库实战 |
| Streamlit 构建 AI 应用 | [B站搜索：Streamlit AI 应用](https://search.bilibili.com/all?keyword=Streamlit+AI+%E5%BA%94%E7%94%A8) | 给项目加界面 |

---

## 八、B站与学习资源推荐

### 8.1 完整学习路径视频

| 序号 | 教程名称 | 推荐链接/BV号 | 适合阶段 |
|------|---------|-------------|---------|
| 1 | Python 零基础全套 | [BV1WgVr6REPJ](https://www.bilibili.com/video/BV1WgVr6REPJ/) | 阶段一 |
| 2 | AI Agent 精华讲解（35分钟） | [BV1dxm6YPEDB](https://www.bilibili.com/video/BV1dxm6YPEDB/) | 阶段二 |
| 3 | Agent 智能体开发全套教程 | [BV1gNVm6pEeQ](https://www.bilibili.com/video/BV1gNVm6pEeQ/) | 阶段三~六 |
| 4 | AI Agent 从入门到精通 | [BV1Z7ZwYHENT](https://www.bilibili.com/video/BV1Z7ZwYHENT/) | 阶段五 |
| 5 | Python+AI 大模型零基础到进阶 | [BV1sTAwzTEJL](https://www.bilibili.com/video/BV1sTAwzTEJL/) | 全阶段 |

### 8.2 图文教程/在线文档

| 资源 | 链接 | 说明 |
|------|------|------|
| 菜鸟教程 AI Agent | [runoob.com/ai-agent](https://www.runoob.com/ai-agent/ai-agent-tutorial.html) | 最友好的入门图文教程 |
| Hello-Agents（Datawhale） | [github.com/datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | 开源入门教程，中文 |
| ai-agents-from-zero | [github.com/didilili/ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero) | 2026 最系统的速成指南 |
| LearnAgent | [learnagent.org](https://learnagent.org/start/) | 入门学习路径网站 |

### 8.3 免费 API 平台（练手用）

| 平台 | 特点 | 链接 |
|------|------|------|
| **DeepSeek** | 性价比最高，¥1/百万Token | platform.deepseek.com |
| **SiliconFlow** | 免费额度，支持多种开源模型 | siliconflow.cn |
| **阿里百炼** | 通义千问 API，有免费额度 | dashscope.aliyun.com |
| **智谱 AI** | GLM 系列，有免费额度 | open.bigmodel.cn |

---

## 九、书单推荐

### 必读 3 本

| 序号 | 书名 | 作者/出版社 | 理由 |
|------|------|-----------|------|
| 1 | **《大模型应用开发极简入门》** | Olivier Caelen / O'Reilly | 最适合初学者的 LLM 实战书，含 Agent 章节 |
| 2 | **《LangChain 编程：从入门到实践》** | 狼书工作室 | 中文最佳 LangChain/Agent 实战书 |
| 3 | **《用 Python 动手学机器学习》** | 伊藤真 | 图文并茂，零基础友好 |

### 选读 2 本

| 序号 | 书名 | 说明 |
|------|------|------|
| 4 | 《Python 编程：从入门到实践》 | Python 经典入门书，需要系统学 Python 时读 |
| 5 | Anthropic《Building Effective Agents》 | 免费，Agent 工程最佳实践指南 |

---

## 学习节奏建议

```
┌────────────────────────────────────────────────────┐
│                    16 周学习计划                      │
├────────┬────────────────────────────────────────────┤
│ 第1-3周 │ 阶段一：Python 速成                          │
│        │ 每天 1-2h：变量→函数→dict→HTTP 请求           │
│        │ 有 Python 基础直接跳过                       │
├────────┼────────────────────────────────────────────┤
│ 第4-5周 │ 阶段二：AI 与大模型基础认知                    │
│        │ 每天 1h：概念理解 + 看科普视频                 │
│        │ 不需要写代码，重点是理解                       │
├────────┼────────────────────────────────────────────┤
│ 第6-8周 │ 阶段三：LLM API 调用入门                     │
│        │ 每天 1.5h：注册 API → 第一次调用 → 多轮对话     │
│        │ 关键里程碑：能跑通第一个 API 调用               │
├────────┼────────────────────────────────────────────┤
│ 第9-10周│ 阶段四：Prompt 工程基础                      │
│        │ 每天 1.5h：写 Prompt → 调优 → 对比效果         │
│        │ 重点：学会结构化 Prompt 模板                   │
├────────┼────────────────────────────────────────────┤
│ 第11-14周│ 阶段五：第一个 AI Agent                     │
│        │ 每天 2h：理解 ReAct → 写 Agent 循环            │
│        │ → 加工具 → 加界面（Streamlit）                │
│        │ 关键里程碑：Agent 能自主调用工具完成任务        │
├────────┼────────────────────────────────────────────┤
│ 第15-16周│ 阶段六：RAG 入门 + 综合项目                  │
│        │ 每天 2h：向量数据库 → RAG 问答 → 知识库项目     │
│        │ 最终产出：可演示的个人知识库 Agent              │
└────────┴────────────────────────────────────────────┘
```

### 每日节奏（适合在职学习）

```
周一~周五：
  晚上 1.5-2h：看视频 + 写代码
  通勤/午休 20min：看一篇技术文章

周六（重点日）：
  上午 2-3h：系统学习新内容
  下午 2h：动手写代码，跑通示例

周日（弹性）：
  上午 1-2h：复习 + 整理笔记
  下午：休息 / 补进度
```

---

## 学完检验标准

### ✅ 你应该能做到

- [ ] 用 Python 调用 DeepSeek/GPT API 完成文本生成
- [ ] 写出结构化的 Prompt，控制模型输出格式
- [ ] 理解 Agent = LLM + 工具 + 循环决策
- [ ] 独立写出包含 2-3 个工具的 Agent 循环代码
- [ ] 理解 RAG 的原理，能用 ChromaDB 搭建简单知识库问答
- [ ] 用 Streamlit 给 Agent 加上 Web 界面
- [ ] 有一个完整的 Agent 项目可以演示

### ❌ 你还不需要

- 理解 Transformer 底层原理
- 掌握多 Agent 协作
- 了解 MCP/A2A 协议
- 微调/训练模型
- 处理高并发生产环境

---

## 关键提醒

1. **先动手，再理解**：不要试图先搞懂所有理论再写代码。把代码跑起来，看到效果，再回头理解原理
2. **API Key 是入场券**：花 10 块钱充值 DeepSeek，马上就能开始实战
3. **完成比完美重要**：第一个 Agent 可以很简陋，重要的是跑通整个流程
4. **善用 AI 辅助学习**：遇到不懂的代码，直接问 ChatGPT/DeepSeek 解释
5. **坚持输出**：每学完一个阶段，写一篇简短的笔记或发一条朋友圈

---

> **学完初级路线后，可无缝衔接：[中级 AI Agent 工程师学习路线](./ai-agent-intermediate-roadmap.md)**
>
> **三阶段路线图已齐全**：
> - 初级（本文）→ [中级](./ai-agent-intermediate-roadmap.md) → [高级](./ai-agent-advanced-roadmap.md)
> - 4-6 个月 → 4-6 个月 → 4-6 个月
