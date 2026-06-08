# 中级 AI Agent 工程师学习路线

> 适用阶段：1-2 年软件开发经验，有 Python 基础，从传统开发转向 AI Agent 工程
> 更新日期：2026年6月
> 前置条件：已掌握初级 AI Agent 基础（或已完成初级路线）

---

## 目录

1. [能力模型总览](#一能力模型总览)
2. [阶段一：LLM 应用层深度掌握（3-4 周）](#二阶段一llm-应用层深度掌握)
3. [阶段二：Prompt 工程进阶（2-3 周）](#三阶段二prompt-工程进阶)
4. [阶段三：单 Agent 全链路开发（4-5 周）](#四阶段三单-agent-全链路开发)
5. [阶段四：RAG 实战进阶（3-4 周）](#五阶段四rag-实战进阶)
6. [阶段五：Agent 评估与工程化（2-3 周）](#六阶段五agent-评估与工程化)
7. [阶段六：项目实战与面试突击（4 周）](#七阶段六项目实战与面试突击)
8. [B站与学习资源推荐](#八b站与学习资源推荐)
9. [书单推荐](#九书单推荐)

---

## 一、能力模型总览

```
                      中级 AI Agent 工程师
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐          ┌────▼────┐
   │ LLM应用层 │          │ Agent开发  │          │ 工程落地 │
   │          │          │            │          │          │
   │• 模型API深度调用│     │• Tool Calling│        │• RAG全链路   │
   │• Token/成本优化 │     │• Memory系统  │        │• 评估体系    │
   │• 结构化输出     │     │• LangChain   │        │• 可观测性    │
   │• 模型选型与路由 │     │• LangGraph   │        │• 部署上线    │
   │• 流式处理       │     │• 错误处理    │        │• 安全防护    │
   └──────────┘          └─────────────┘        └──────────┘
```

### AI Agent 工程师三级进阶定位

| 层级 | 角色 | 核心能力 | 本文定位 |
|------|------|---------|---------|
| **初级** | Agent 使用者 | 会用 API、能跑通 Demo、了解基本概念 | ← 前置 |
| **中级** | Agent 开发者 | **能独立构建可落地的 Agent 系统** | **本文** |
| **高级** | Agent 架构师 | 多 Agent 编排、MCP/A2A 协议、企业级治理 | → 进阶 |

### 初级 → 中级 核心转变

```
初级：能调 API、会用 LangChain 跑 Demo、复制粘贴 Prompt
         ↓  关键突破
中级：理解 Agent 全链路原理、能独立设计 Agent 架构、
       会排查线上问题、能写可上生产的 Agent 代码
```

---

## 二、阶段一：LLM 应用层深度掌握

> **周期**：3-4 周  
> **目标**：从"会用 API"到"精通 API 的各种高级用法"

### 2.1 模型 API 深度调用

#### OpenAI/DeepSeek API 全特性

```python
# 1. 基础补全 vs 流式补全
from openai import OpenAI

client = OpenAI()

# 非流式（等全部生成完再返回）
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "解释Transformer"}],
    temperature=0.7,
    max_tokens=2048,
)

# 流式（逐 token 返回，提升用户体验）
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "解释Transformer"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

```python
# 2. 结构化输出（JSON Mode / Structured Outputs）
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "提取：张三，28岁，北京，Java工程师"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "city": {"type": "string"},
                    "job": {"type": "string"},
                },
                "required": ["name", "age", "city", "job"],
            },
        },
    },
)
print(response.choices[0].message.content)
# {"name":"张三","age":28,"city":"北京","job":"Java工程师"}
```

```python
# 3. 多模态调用（图片理解）
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这张图片里有什么？"},
            {"type": "image_url", "image_url": {"url": "https://example.com/photo.jpg"}},
        ],
    }],
)
```

#### 核心掌握点

| 能力点 | 关键细节 | 实践要点 |
|--------|---------|---------|
| **流式处理** | SSE 协议、chunk 拼接、断线重连 | 实现打字机效果、处理 `[DONE]` 标记 |
| **结构化输出** | JSON Mode、JSON Schema 约束 | 与下游系统解耦、减少解析错误 |
| **多轮对话** | 上下文窗口管理、消息截断策略 | 滑动窗口、摘要压缩、Token 计数 |
| **错误处理** | Rate Limit、Token 超限、服务不可用 | 指数退避重试、降级策略 |

### 2.2 Token 与成本优化

```python
import tiktoken

# Token 计数
encoding = tiktoken.encoding_for_model("gpt-4o")
tokens = encoding.encode("Hello, world!")
print(f"Token 数: {len(tokens)}")  # Token 数: 4

# 估算成本
# GPT-4o: $2.50/1M input tokens, $10/1M output tokens
# DeepSeek: ¥1/1M input tokens, ¥2/1M output tokens

def estimate_cost(input_text: str, output_length: int, model: str = "gpt-4o") -> float:
    encoding = tiktoken.encoding_for_model(model)
    input_tokens = len(encoding.encode(input_text))
    # 简化计算
    cost_per_1m_input = 2.5   # $2.50
    cost_per_1m_output = 10.0  # $10.00
    total = (input_tokens / 1_000_000) * cost_per_1m_input + \
            (output_length / 1_000_000) * cost_per_1m_output
    return total
```

**成本优化策略**：
1. **缓存常见回答**：相同问题走缓存，不调 API
2. **压缩上下文**：用 LLM 先摘要历史对话再送入
3. **模型降级**：简单任务用更便宜的模型（如 DeepSeek-V3 vs GPT-4o）
4. **批处理**：合并多个请求（Batch API）

### 2.3 模型选型与路由

```
任务类型               推荐模型              理由
──────────────────────────────────────────────────
简单文本生成          DeepSeek-V3          性价比最高
复杂推理/代码         Claude 4 / GPT-4o    最强推理能力
多模态理解            GPT-4o / Gemini 2.5  原生多模态
超长上下文(100K+)     Gemini 2.5 Flash     1M token 窗口
中文场景              DeepSeek / Qwen3     中文理解最优
离线/私有化           Qwen3 / Llama 4      开源可部署
```

```python
# 模型路由器：根据任务自动选择模型
class ModelRouter:
    def __init__(self):
        self.routes = {
            "simple": "deepseek-chat",
            "complex": "gpt-4o",
            "multimodal": "gpt-4o",
            "chinese": "deepseek-chat",
            "code": "claude-sonnet-4-20250514",
        }

    def route(self, task_type: str, has_image: bool = False) -> str:
        if has_image:
            return self.routes["multimodal"]
        return self.routes.get(task_type, "deepseek-chat")
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| OpenAI API 实战指南 | [B站搜索：OpenAI API 完整教程](https://search.bilibili.com/all?keyword=OpenAI+API+%E5%AE%8C%E6%95%B4%E6%95%99%E7%A8%8B) | API 全特性实战 |
| Token 与成本控制 | [B站搜索：大模型 Token 计费原理](https://search.bilibili.com/all?keyword=%E5%A4%A7%E6%A8%A1%E5%9E%8B+token+%E8%AE%A1%E8%B4%B9) | 理解计费与优化 |

---

## 三、阶段二：Prompt 工程进阶

> **周期**：2-3 周  
> **目标**：从"随便写 Prompt"到"工程化设计 Prompt"

### 3.1 进阶 Prompt 技术

#### Chain of Thought (CoT) — 思维链

```python
# ❌ 直接问（容易出错）
prompt_bad = "我有 15 个苹果，给了小明 3 个，又买了 7 个，现在有几个？"

# ✅ CoT 引导（大幅提升推理准确率）
prompt_good = """
我有 15 个苹果，给了小明 3 个，又买了 7 个，现在有几个？

让我们一步一步思考：
1. 初始：15 个苹果
2. 给出 3 个后：15 - 3 = 12 个
3. 买了 7 个后：12 + 7 = 19 个
所以答案是：19 个
"""
```

#### ReAct (Reasoning + Acting)

```python
# ReAct 模式：思考 → 行动 → 观察 → 思考 → ...
react_prompt = """
你是一个能使用工具的智能助手。请按以下格式回答：

Thought: 我需要思考下一步做什么
Action: 要调用的工具名
Action Input: 工具输入参数
Observation: 工具返回结果
...（可重复多轮）
Thought: 我已经有足够信息回答
Final Answer: 最终回答

用户问题：今天北京天气怎么样？适合户外运动吗？
"""
```

#### Few-Shot 与动态示例选择

```python
# Few-Shot：给模型几个示例让它学会模式
few_shot_prompt = """
将以下句子分类为「正面」或「负面」：

示例1：
句子：这家餐厅很好吃
分类：正面

示例2：
句子：服务态度太差了
分类：负面

示例3：
句子：价格有点贵，但味道不错
分类：正面

现在请分类：
句子：{user_input}
分类：
"""

# 动态示例选择（RAG 方式检索最相关的示例）
def select_examples(user_input: str, example_pool: list, k: int = 3):
    """从示例池中检索最相关的 k 个示例"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    all_texts = [user_input] + [e["input"] for e in example_pool]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    top_k_idx = similarities.argsort()[-k:][::-1]
    return [example_pool[i] for i in top_k_idx]
```

### 3.2 Prompt 模板工程化

```python
# Prompt 版本管理与 A/B 测试
from dataclasses import dataclass
from typing import Optional

@dataclass
class PromptTemplate:
    name: str
    version: str
    system_prompt: str
    user_template: str
    variables: list[str]

# 注册多个版本
prompts = {
    "v1.0": PromptTemplate(
        name="客服助手",
        version="1.0",
        system_prompt="你是一个客服助手，请礼貌回答用户问题。",
        user_template="用户：{query}",
        variables=["query"],
    ),
    "v1.1": PromptTemplate(
        name="客服助手",
        version="1.1",
        system_prompt="你是{company}的客服助手，请用专业、友好的语气回答。如无法回答，请引导用户联系人工客服。",
        user_template="用户问题：{query}\n用户等级：{level}",
        variables=["company", "query", "level"],
    ),
}

def render_prompt(template: PromptTemplate, **kwargs) -> dict:
    """渲染 Prompt 模板"""
    return {
        "system": template.system_prompt.format(**kwargs),
        "user": template.user_template.format(**kwargs),
    }
```

### 3.3 Prompt 评测与优化

```python
# Prompt 评测框架
def evaluate_prompt(prompt_template, test_cases: list[dict], judge_model: str = "gpt-4o"):
    """用 LLM-as-Judge 评测 Prompt 效果"""
    results = []
    for case in test_cases:
        # 调用模型
        response = call_llm(prompt_template, case["input"])
        # LLM 评判
        judge_prompt = f"""
        评估以下回答质量（1-5分）：
        用户问题：{case['input']}
        期望答案：{case['expected']}
        实际回答：{response}
        
        评分标准：
        1分：完全错误或无关
        2分：部分相关但有明显错误
        3分：基本正确但不够完整
        4分：正确且完整
        5分：超出预期
        
        请只输出分数（数字）：
        """
        score = int(call_llm_simple(judge_prompt, model=judge_model))
        results.append({"input": case["input"], "expected": case["expected"],
                        "actual": response, "score": score})
    avg_score = sum(r["score"] for r in results) / len(results)
    return avg_score, results
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| Prompt 工程完全指南 | [B站搜索：Prompt Engineering 完整教程](https://search.bilibili.com/all?keyword=Prompt+Engineering+%E5%AE%8C%E6%95%B4%E6%95%99%E7%A8%8B) | 从 CoT 到 ReAct |
| 结构化 Prompt 设计 | [B站搜索：结构化Prompt设计](https://search.bilibili.com/all?keyword=%E7%BB%93%E6%9E%84%E5%8C%96Prompt) | 工程化实践 |

---

## 四、阶段三：单 Agent 全链路开发

> **周期**：4-5 周  
> **目标**：独立开发可落地的单 Agent 系统

### 4.1 Tool Calling（工具调用）— Agent 的核心能力

#### OpenAI Function Calling 实战

```python
import json
from openai import OpenAI

client = OpenAI()

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的实时天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网获取最新信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "num_results": {"type": "integer", "description": "返回结果数量"},
                },
                "required": ["query"],
            },
        },
    },
]

# 工具执行函数
def execute_tool(tool_name: str, arguments: dict) -> str:
    if tool_name == "get_weather":
        # 实际项目中调用天气 API
        return f"{arguments['city']}：晴，25°C，湿度 60%"
    elif tool_name == "search_web":
        return f"搜索结果：关于 '{arguments['query']}' 的 3 条结果..."
    return "未知工具"

# Agent 循环
def agent_loop(user_query: str, max_turns: int = 5) -> str:
    messages = [{"role": "user", "content": user_query}]

    for turn in range(max_turns):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        # 如果模型直接返回文本答案
        if not msg.tool_calls:
            return msg.content

        # 处理工具调用
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            result = execute_tool(func_name, func_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    return "达到最大轮次，未能完成任务"

# 使用
result = agent_loop("北京今天天气怎么样？适合出去玩吗？")
print(result)
```

#### 工具设计最佳实践

```python
# 工具设计原则
TOOL_DESIGN_RULES = """
1. 单一职责：每个工具只做一件事
2. 清晰描述：description 要详细，帮助模型正确选择工具
3. 参数校验：在工具内部做参数校验，不要信任模型传参
4. 错误处理：返回结构化的错误信息，方便模型理解并重试
5. 超时控制：外部 API 调用必须设超时
6. 幂等性：读操作天然幂等，写操作需要考虑去重
"""

# 好的工具定义示例
good_tool = {
    "type": "function",
    "function": {
        "name": "create_order",
        "description": "创建新订单。当用户明确表示要下单购买商品时使用。\n"
                       "注意：创建前需要确认用户已选择商品和数量。",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "商品ID，格式为 PROD-XXXX",
                },
                "quantity": {
                    "type": "integer",
                    "description": "购买数量，必须大于0",
                    "minimum": 1,
                },
                "idempotent_key": {
                    "type": "string",
                    "description": "幂等键，用于防止重复下单",
                },
            },
            "required": ["product_id", "quantity", "idempotent_key"],
        },
    },
}
```

### 4.2 Memory 系统设计

```python
from typing import TypedDict
from datetime import datetime

# Memory 类型
class MemoryType:
    SHORT_TERM = "short_term"    # 会话内记忆（当前对话）
    LONG_TERM = "long_term"      # 长期记忆（跨会话）
    WORKING = "working"          # 工作记忆（当前任务中间状态）

# Memory 系统实现
class AgentMemory:
    def __init__(self, max_short_term: int = 20):
        self.short_term: list[dict] = []      # 最近 N 轮对话
        self.long_term: dict[str, list] = {}   # key: user_id → 历史摘要
        self.working: dict = {}               # 当前任务中间结果
        self.max_short_term = max_short_term

    def add_message(self, role: str, content: str):
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        # 超出上限时压缩
        if len(self.short_term) > self.max_short_term * 2:
            self._compress()

    def _compress(self):
        """将旧消息压缩为摘要"""
        old_messages = self.short_term[:-self.max_short_term]
        summary = summarize_conversation(old_messages)  # 调用 LLM 摘要
        self.long_term.setdefault("summaries", []).append(summary)
        self.short_term = self.short_term[-self.max_short_term:]

    def get_context(self) -> list[dict]:
        """获取完整上下文（长期摘要 + 短期对话）"""
        context = []
        # 加入长期记忆摘要
        for summary in self.long_term.get("summaries", [])[-3:]:
            context.append({"role": "system", "content": f"[历史摘要] {summary}"})
        # 加入短期记忆
        context.extend(self.short_term)
        return context

    def save_working(self, key: str, value):
        self.working[key] = value

    def get_working(self, key: str):
        return self.working.get(key)
```

### 4.3 LangChain 实战

> **重要提醒**：先用原生 SDK 理解 Agent 本质，再用 LangChain 提效。  
> 参考 Anthropic 的建议：不要一上来就用框架。

```python
# LangChain 方式构建 Agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 定义工具（用 @tool 装饰器）
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 实际调用天气 API
    return f"{city}今天晴，25°C"

@tool
def calculator(expression: str) -> str:
    """计算数学表达式，如：'2+3*4'"""
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# 2. 创建 Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [get_weather, calculator]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，可以使用工具来回答用户问题。"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,
)

# 3. 执行
result = agent_executor.invoke({"input": "北京天气怎么样？3乘以7是多少？"})
print(result["output"])
```

### 4.4 LangGraph — 状态图式 Agent

```python
# LangGraph：用图来定义 Agent 的工作流
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]  # 自动追加
    next_action: str
    final_answer: str

# 定义节点
def think(state: AgentState) -> AgentState:
    """思考节点：调用 LLM 决定下一步"""
    response = llm.invoke(state["messages"])
    # 解析响应，决定是调用工具还是直接回答
    return {"messages": [response], "next_action": "tool" if has_tool_call(response) else "answer"}

def execute_tools(state: AgentState) -> AgentState:
    """执行工具调用"""
    # 执行 tools...
    return {"messages": [tool_result]}

def answer(state: AgentState) -> AgentState:
    """生成最终回答"""
    return {"final_answer": state["messages"][-1].content}

# 构建图
workflow = StateGraph(AgentState)
workflow.add_node("think", think)
workflow.add_node("tools", execute_tools)
workflow.add_node("answer", answer)

workflow.set_entry_point("think")
workflow.add_conditional_edges(
    "think",
    lambda s: s["next_action"],
    {"tool": "tools", "answer": "answer"},
)
workflow.add_edge("tools", "think")
workflow.add_edge("answer", END)

app = workflow.compile()
result = app.invoke({"messages": [{"role": "user", "content": "北京天气？"}]})
```

### 4.5 错误处理与韧性设计

```python
import time
from functools import wraps

# 重试装饰器（指数退避）
def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    if attempt == max_retries:
                        raise
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    time.sleep(base_delay)
            return None
        return wrapper
    return decorator

# Agent 安全边界
class AgentGuardrails:
    """Agent 安全护栏"""
    FORBIDDEN_ACTIONS = ["delete_database", "format_system", "send_email_all"]

    @staticmethod
    def validate_tool_call(tool_name: str, arguments: dict) -> bool:
        if tool_name in AgentGuardrails.FORBIDDEN_ACTIONS:
            return False
        return True

    @staticmethod
    def validate_output(output: str) -> str:
        """过滤敏感信息"""
        # 脱敏手机号、身份证等
        import re
        output = re.sub(r'1[3-9]\d{9}', '****', output)
        return output
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| AI Agent 全栈开发教程 | [BV1UZEN6CEA3](https://www.bilibili.com/video/BV1UZEN6CEA3/) | LangChain+LangGraph+RAG 全覆盖 |
| LangChain Agent 实战 | [B站搜索：LangChain Agent 实战](https://search.bilibili.com/all?keyword=LangChain+Agent+%E5%AE%9E%E6%88%98) | 工具调用+记忆系统 |
| LangGraph 图式 Agent | [B站搜索：LangGraph 教程](https://search.bilibili.com/all?keyword=LangGraph+%E6%95%99%E7%A8%8B) | 状态图实战 |

---

## 五、阶段四：RAG 实战进阶

> **周期**：3-4 周  
> **目标**：从基础 RAG 到能处理复杂检索场景

### 5.1 RAG 全链路深入

```python
# RAG 完整 Pipeline
class RAGPipeline:
    def __init__(self):
        self.chunker = TextChunker()
        self.embedder = EmbeddingModel()
        self.vector_store = VectorStore()
        self.retriever = HybridRetriever()
        self.reranker = Reranker()
        self.generator = LLMGenerator()

    def ingest(self, documents: list[str]):
        """文档入库"""
        for doc in documents:
            # 1. 分块（考虑语义边界）
            chunks = self.chunker.split(doc, chunk_size=500, overlap=50)
            # 2. 向量化
            embeddings = self.embedder.encode(chunks)
            # 3. 存入向量库
            self.vector_store.add(chunks, embeddings)

    def query(self, question: str, top_k: int = 5) -> str:
        """查询流程"""
        # 1. 混合检索（向量 + 关键词）
        candidates = self.retriever.search(question, top_k=top_k * 2)
        # 2. 重排序
        ranked = self.reranker.rerank(question, candidates)[:top_k]
        # 3. 生成回答（带引用）
        context = "\n\n".join([c.content for c in ranked])
        answer = self.generator.generate(question, context, with_citations=True)
        return answer
```

### 5.2 分块策略

```python
class TextChunker:
    """智能文本分块"""

    @staticmethod
    def fixed_size(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """固定大小分块（最简单）"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    @staticmethod
    def semantic_split(text: str, separators: list[str] = None) -> list[str]:
        """按语义边界分块（推荐）"""
        if separators is None:
            separators = ["\n\n", "\n", "。", ".", "；", ";", " "]
        # 递归按分隔符切分
        return recursive_split(text, separators, chunk_size=500)

    @staticmethod
    def sentence_aware_split(text: str, max_sentences: int = 5) -> list[str]:
        """按句子分块，保持语义完整"""
        import re
        sentences = re.split(r'(?<=[。！？.!?])\s*', text)
        chunks = []
        for i in range(0, len(sentences), max_sentences):
            chunk = "".join(sentences[i:i + max_sentences])
            chunks.append(chunk)
        return chunks
```

### 5.3 混合检索 + 重排序

```python
class HybridRetriever:
    """混合检索：向量相似度 + BM25 关键词"""

    def __init__(self, vector_store, bm25_index):
        self.vector_store = vector_store
        self.bm25 = bm25_index

    def search(self, query: str, top_k: int = 10, alpha: float = 0.7) -> list:
        # 向量检索
        vector_results = self.vector_store.similarity_search(query, k=top_k)

        # 关键词检索（BM25）
        keyword_results = self.bm25.search(query, k=top_k)

        # 融合排序（加权 Reciprocal Rank Fusion）
        fused = self._rrf_fusion(vector_results, keyword_results, alpha)
        return fused[:top_k]

    @staticmethod
    def _rrf_fusion(results_a, results_b, alpha, k=60):
        """RRF 融合算法"""
        scores = {}
        for rank, item in enumerate(results_a):
            scores[item.id] = scores.get(item.id, 0) + alpha / (k + rank + 1)
        for rank, item in enumerate(results_b):
            scores[item.id] = scores.get(item.id, 0) + (1 - alpha) / (k + rank + 1)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### 5.4 RAG 评估

```python
# RAG 评估指标
def evaluate_rag(queries: list[str], ground_truth: list[str]) -> dict:
    """RAG 系统评估"""
    results = {"faithfulness": [], "answer_relevancy": [], "context_recall": []}

    for query, truth in zip(queries, ground_truth):
        # 检索
        contexts = retrieve(query)
        # 生成
        answer = generate(query, contexts)

        # 忠实度：回答是否忠于检索到的上下文
        results["faithfulness"].append(calc_faithfulness(answer, contexts))

        # 答案相关性：回答是否切题
        results["answer_relevancy"].append(calc_relevancy(query, answer))

        # 上下文召回率：检索是否覆盖了回答所需信息
        results["context_recall"].append(calc_recall(contexts, truth))

    return {k: sum(v)/len(v) for k, v in results.items()}
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| RAG 从入门到精通 | [B站搜索：RAG 从零到一 完整实战](https://search.bilibili.com/all?keyword=RAG+%E4%BB%8E%E9%9B%B6%E5%88%B0%E4%B8%80+%E5%AE%8C%E6%95%B4%E5%AE%9E%E6%88%98) | 全链路 RAG 实战 |
| 混合检索与重排序 | [B站搜索：RAG 混合检索 重排序](https://search.bilibili.com/all?keyword=RAG+%E6%B7%B7%E5%90%88%E6%A3%80%E7%B4%A2+%E9%87%8D%E6%8E%92%E5%BA%8F) | 进阶检索策略 |

---

## 六、阶段五：Agent 评估与工程化

> **周期**：2-3 周  
> **目标**：让 Agent 从 Demo 变成可上线系统

### 6.1 Agent 评估体系

```python
# 多维评估框架
class AgentEvaluator:
    def __init__(self, judge_model: str = "gpt-4o"):
        self.judge_model = judge_model
        self.metrics = [
            "task_completion",    # 任务完成度
            "tool_accuracy",      # 工具选择准确率
            "efficiency",         # 效率（轮次/Token）
            "safety",            # 安全性
            "user_satisfaction",  # 用户满意度
        ]

    def evaluate_run(self, task: str, agent_trace: dict) -> dict:
        """评估一次 Agent 运行"""
        scores = {}
        scores["task_completion"] = self._judge_completion(task, agent_trace)
        scores["tool_accuracy"] = self._judge_tool_accuracy(agent_trace)
        scores["efficiency"] = self._calc_efficiency(agent_trace)
        scores["safety"] = self._judge_safety(agent_trace)
        return scores

    def benchmark(self, test_suite: list[dict]) -> dict:
        """批量评估"""
        all_scores = []
        for test in test_suite:
            trace = run_agent(test["task"])
            scores = self.evaluate_run(test["task"], trace)
            all_scores.append(scores)

        # 汇总
        avg_scores = {}
        for metric in self.metrics:
            avg_scores[metric] = sum(s[metric] for s in all_scores) / len(all_scores)
        return avg_scores
```

### 6.2 可观测性

```python
# Agent 运行追踪
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger("agent")

@contextmanager
def trace_step(step_name: str):
    """追踪 Agent 每一步的执行"""
    start = time.time()
    step_id = f"{step_name}_{int(start)}"
    logger.info(f"[{step_id}] 开始: {step_name}")
    try:
        yield step_id
        elapsed = time.time() - start
        logger.info(f"[{step_id}] 完成: {step_name} (耗时 {elapsed:.2f}s)")
    except Exception as e:
        elapsed = time.time() - start
        logger.error(f"[{step_id}] 失败: {step_name} (耗时 {elapsed:.2f}s) - {e}")
        raise

# 使用
with trace_step("tool_call:get_weather") as step_id:
    result = get_weather("北京")
    # 记录到可观测平台（如 LangFuse）
    log_to_observability(step_id, result)
```

### 6.3 部署与 API 化

```python
# FastAPI 部署 Agent
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="AI Agent Service")

class AgentRequest(BaseModel):
    query: str
    user_id: str
    session_id: str | None = None
    stream: bool = False

class AgentResponse(BaseModel):
    answer: str
    session_id: str
    tool_calls: list = []
    tokens_used: int = 0

@app.post("/agent/chat", response_model=AgentResponse)
async def chat(request: AgentRequest):
    try:
        # 获取或创建会话
        session = get_or_create_session(request.session_id or request.user_id)

        # 执行 Agent
        result = agent_loop(
            query=request.query,
            memory=session.memory,
            user_id=request.user_id,
        )
        return AgentResponse(
            answer=result["answer"],
            session_id=session.id,
            tool_calls=result.get("tool_calls", []),
            tokens_used=result.get("tokens_used", 0),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 流式端点
@app.post("/agent/chat/stream")
async def chat_stream(request: AgentRequest):
    from fastapi.responses import StreamingResponse
    async def generate():
        async for chunk in agent_stream(request.query, request.user_id):
            yield f"data: {json.dumps(chunk)}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| Agent 评估与监控 | [B站搜索：AI Agent 评估 LangFuse](https://search.bilibili.com/all?keyword=AI+Agent+%E8%AF%84%E4%BC%B0+LangFuse) | 可观测性实战 |
| FastAPI 部署 Agent | [B站搜索：FastAPI 部署 AI 应用](https://search.bilibili.com/all?keyword=FastAPI+%E9%83%A8%E7%BD%B2+AI) | API 化部署 |

---

## 七、阶段六：项目实战与面试突击

> **周期**：4 周  
> **目标**：完成 2 个可写入简历的实战项目 + 通过面试

### 7.1 必做项目一：智能客服 Agent

```
项目：企业知识库智能客服 Agent
周期：2 周

技术栈：
├── LangChain / 原生 SDK
├── RAG（混合检索 + 重排序）
├── Tool Calling（订单查询、工单创建）
├── Memory（多轮对话上下文）
├── FastAPI 部署

核心功能：
1. 基于企业知识库的 RAG 问答
2. 自动识别意图，调用对应工具
3. 多轮对话上下文理解
4. 无法回答时转人工
5. 对话质量评估

亮点：
- 实现了混合检索（向量 + BM25）提升召回率
- 加入了重排序模型提升准确率
- 完善的错误处理和降级策略
```

### 7.2 必做项目二：数据分析 Agent

```
项目：自然语言数据分析 Agent
周期：2 周

技术栈：
├── LangGraph 状态图
├── Function Calling（SQL 生成、图表绘制）
├── Pandas + Matplotlib
├── Streamlit / Gradio 前端

核心功能：
1. 自然语言转 SQL 查询数据库
2. 自动生成可视化图表
3. 多步骤分析流程（问 → 查 → 算 → 画图 → 总结）
4. 分析结果可导出

亮点：
- LangGraph 定义多步骤分析工作流
- SQL 安全校验（防注入）
- 自动选择合适的图表类型
```

### 7.3 面试高频考点

| 考点 | 高频问题 | 准备重点 |
|------|---------|---------|
| **Agent 架构** | Agent 由哪些核心组件构成？Tool Calling 原理？ | 能画出架构图，讲清各组件职责 |
| **Prompt 工程** | CoT vs ReAct 区别？如何设计 Few-Shot？ | 结合项目经验讲实际应用 |
| **RAG** | RAG 全链路？如何优化检索？分块策略？ | 混合检索、重排序、评估指标 |
| **Memory** | 短期/长期记忆如何设计？上下文管理？ | 压缩策略、滑动窗口、Token 预算 |
| **工程化** | 如何评估 Agent？错误处理？部署方案？ | 评估体系、降级策略、API 设计 |
| **Function Calling** | 工具定义最佳实践？如何处理工具调用失败？ | 单一职责、错误返回格式 |

### 📺 本阶段推荐视频

| 教程 | 链接 | 说明 |
|------|------|------|
| Agent 面试真题精讲 | [B站搜索：AI Agent 面试题](https://search.bilibili.com/all?keyword=AI+Agent+%E9%9D%A2%E8%AF%95%E9%A2%98) | 高频面试题解析 |
| LangChain 项目实战 | [BV1UZEN6CEA3](https://www.bilibili.com/video/BV1UZEN6CEA3/) | 全栈 Agent 项目 |

---

## 八、B站与学习资源推荐

### 8.1 核心视频教程

| 序号 | 教程名称 | 推荐链接/BV号 | 适合阶段 |
|------|---------|-------------|---------|
| 1 | AI Agent 全栈开发教程 | [BV1UZEN6CEA3](https://www.bilibili.com/video/BV1UZEN6CEA3/) | 阶段三、四 |
| 2 | Python+AI大模型零基础到进阶 | [BV1sTAwzTEJL](https://www.bilibili.com/video/BV1sTAwzTEJL/) | 阶段一、二 |
| 3 | OpenAI API 实战指南 | [B站搜索](https://search.bilibili.com/all?keyword=OpenAI+API+%E5%AE%8C%E6%95%B4%E6%95%99%E7%A8%8B) | 阶段一 |
| 4 | Prompt Engineering 系统教程 | [B站搜索](https://search.bilibili.com/all?keyword=Prompt+Engineering+%E6%95%99%E7%A8%8B) | 阶段二 |
| 5 | LangChain + LangGraph 实战 | [B站搜索](https://search.bilibili.com/all?keyword=LangChain+LangGraph+%E5%AE%9E%E6%88%98) | 阶段三 |
| 6 | RAG 企业级实战 | [B站搜索](https://search.bilibili.com/all?keyword=RAG+%E4%BC%81%E4%B8%9A%E7%BA%A7+%E5%AE%9E%E6%88%98) | 阶段四 |
| 7 | FastAPI + AI 部署 | [B站搜索](https://search.bilibili.com/all?keyword=FastAPI+AI+%E9%83%A8%E7%BD%B2) | 阶段五 |
| 8 | AI Agent 面试突击 | [B站搜索](https://search.bilibili.com/all?keyword=AI+Agent+%E9%9D%A2%E8%AF%95) | 阶段六 |

### 8.2 必关注 GitHub 仓库

| 仓库 | Star 数 | 说明 |
|------|---------|------|
| [ai-agents-from-zero](https://github.com/didilili/ai-agents-from-zero) | 热门 | 2026 最系统 Agent 速成指南 |
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 官方 | LangGraph 官方仓库 |
| [run-llama/llama_index](https://github.com/run-llama/llama_index) | 30K+ | RAG 数据框架 |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | 10K+ | LLM 可观测性平台 |

### 8.3 面试题库

| 资源 | 链接 | 说明 |
|------|------|------|
| JavaGuide AI 面试指南 | [javaguide.cn/ai](https://javaguide.cn/ai/interview-questions/ai-interview-guide.html) | 系统整理高频考点 |
| 小林 Coding Agent 面试题 | [xiaolincoding.com](https://xiaolincoding.com/project/xiaolinnote.html) | 2026 最新真题 |
| 代码随想录大模型面经 | [programmercarl.com](https://programmercarl.com/qita/0022.llminterview.html) | 覆盖 RAG/Agent 等 |

---

## 九、书单推荐

### 必读 3 本

| 序号 | 书名 | 作者/出版社 | 理由 |
|------|------|-----------|------|
| 1 | **《大模型应用开发极简入门》** | Olivier Caelen / O'Reilly | 快速上手 LLM 应用开发，含 Agent 实战 |
| 2 | **《LangChain 编程：从入门到实践》** | 狼书工作室 | LangChain/LangGraph 最佳中文实战书 |
| 3 | **《大规模语言模型：从理论到实践》** | 复旦团队 | LLM 底层原理最佳中文入门 |

### 选读 3 本

| 序号 | 书名 | 说明 |
|------|------|------|
| 4 | 《Designing Machine Learning Systems》 | MLOps 思维，理解生产化 |
| 5 | 《Prompt Engineering for LLMs》 | Prompt 工程系统方法论 |
| 6 | Anthropic《Building Effective Agents》 | 免费，Agent 工程纲领性指南 |

---

## 学习节奏建议

```
┌────────────────────────────────────────────────────┐
│                    16 周学习计划                      │
├────────┬────────────────────────────────────────────┤
│ 第1-4周 │ 阶段一：LLM 应用层深度掌握                    │
│        │ 每天 2h：API 调用 → Token优化 → 模型路由      │
├────────┼────────────────────────────────────────────┤
│ 第5-6周 │ 阶段二：Prompt 工程进阶                      │
│        │ 每天 2h：CoT/ReAct → Few-Shot → 评测体系      │
├────────┼────────────────────────────────────────────┤
│ 第7-11周│ 阶段三：单 Agent 全链路开发                   │
│        │ 每天 2-3h：Tool Calling → Memory → LangChain │
│        │ → LangGraph → 错误处理                       │
├────────┼────────────────────────────────────────────┤
│ 第12-14周│ 阶段四+五：RAG实战 + 评估工程化              │
│        │ 每天 2-3h：全链路RAG → 混合检索 → 评估→部署    │
├────────┼────────────────────────────────────────────┤
│ 第15-16周│ 阶段六：项目实战 + 面试突击                  │
│        │ 每天 3h+：2个完整项目 + 刷面试题               │
└────────┴────────────────────────────────────────────┘
```

### 每日节奏

```
周一~周五（工作日）：
  晚上 2-3h：学习 + 写代码
  午休 30min：看技术文章/面试题

周六（深度学习）：
  上午 3h：系统学习新知识
  下午 3h：项目实战

周日（复习巩固）：
  上午 2h：复习本周内容
  下午：自由安排 / 休息
```

---

## 关键提醒

1. **先理解本质，再用框架**：Anthropic 的核心建议——先用原生 SDK 理解 Agent 本质，再考虑用 LangChain 等框架提效
2. **代码量是关键**：中级阶段至少要写 5000+ 行 Agent 相关代码
3. **项目优先于理论**：先动手跑起来，遇到不懂的再回头补理论
4. **面试导向学习**：每个知识点都要能回答"面试会怎么考"
5. **保持输出**：每学完一个阶段写一篇总结博客或笔记

---

> **学完中级路线后，可无缝衔接：[高级 AI Agent 工程师学习路线](./ai-agent-advanced-roadmap.md)**
>
> **三阶段路线图已齐全**：
> - 初级 → 中级（本文）→ 高级
> - 4-6 个月 → 4-6 个月 → 4-6 个月
