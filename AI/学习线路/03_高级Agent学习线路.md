# 高级 AI Agent 工程师学习路线

> 适用阶段：有 3 年+ 软件工程经验，从传统开发转向 AI Agent 高级开发
> 更新日期：2026年6月

---

## 目录

1. [能力模型总览](#一能力模型总览)
2. [阶段一：LLM 底层认知与 Prompt 工程（2-3 周）](#二阶段一llm-底层认知与-prompt-工程)
3. [阶段二：单 Agent 核心开发（3-4 周）](#三阶段二单-agent-核心开发)
4. [阶段三：RAG 与知识增强（2-3 周）](#四阶段三rag-与知识增强)
5. [阶段四：多 Agent 协作与协议（3-4 周）](#五阶段四多-agent-协作与协议)
6. [阶段五：Agent 评估与生产化（3-4 周）](#六阶段五agent-评估与生产化)
7. [阶段六：Agent 架构设计与治理（持续）](#七阶段六agent-架构设计与治理)
8. [B站与学习资源推荐](#八b站与学习资源推荐)
9. [书单推荐](#九书单推荐)

---

## 一、能力模型总览

```
                      高级 AI Agent 工程师
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐          ┌────▼────┐
   │ LLM认知  │          │ Agent核心  │          │ 架构治理 │
   │          │          │            │          │          │
   │• 模型能力边界│       │• Tool Calling│       │• 多Agent编排│
   │• Prompt工程  │       │• ReAct/Plan  │       │• MCP/A2A协议│
   │• Token/上下文│       │• Memory设计  │       │• 评估体系   │
   │• 结构化输出   │       │• RAG全链路   │       │• 安全治理   │
   │• 模型路由     │       │• Human-in-Loop│      │• 成本优化   │
   └──────────┘          └─────────────┘        └──────────┘
```

### AI Agent 三级能力进阶（Anthropic 框架）

| 层级 | 角色 | 核心目标 | 典型产出 |
|------|------|---------|---------|
| **第一阶** | Agent 落地工程师 | 让 Agent 在业务场景"可用" | 单场景智能体原型（客服/运维助手） |
| **第二阶** | Agent 系统工程师 | "稳定、可控、可扩展" | 多 Agent 协作系统、全链路监控 |
| **第三阶** | Agent 架构师 | 全局治理与商业价值 | 企业级 Agent 平台、标准化规范 |

---

## 二、阶段一：LLM 底层认知与 Prompt 工程

> 周期：2-3 周 | 目标：深度理解大模型能力边界，精通 Prompt 设计

### 2.1 大模型核心原理

| 知识点 | 深度要求 | 实践 |
|--------|---------|------|
| Transformer 架构 | 自注意力机制、多头注意力、位置编码 | 阅读 "Attention Is All You Need" |
| Token 与分词 | BPE 分词原理、Token 计数、中英文差异 | 用 tiktoken 计算不同文本的 token 消耗 |
| 上下文窗口 | 窗口限制、注意力衰减、长文本处理策略 | 测试不同窗口大小下的任务效果 |
| 模型能力边界 | 幻觉、逻辑链断裂、知识截止日期、推理深度 | 对同一任务测试 GPT/Claude/Gemini/DeepSeek |
| 推理 vs 训练 | 推理参数（temperature/top_p/top_k）、采样策略 | 对比 temperature=0 和 1.0 的输出差异 |

```python
# 实践：模型对比评估框架
models = {
    "gpt-4o": openai_client,
    "claude-sonnet-4": anthropic_client,
    "deepseek-v3": deepseek_client,
}

test_prompts = [
    "复杂的多步推理题",
    "需要外部知识的问答",
    "代码生成与调试",
    "创意写作",
]

for prompt in test_prompts:
    for name, client in models.items():
        result = client.chat(prompt)
        evaluate(result, metrics=["准确性", "延迟", "成本"])
```

### 2.2 Prompt 工程（核心中的核心）

| 技术 | 说明 | 适用场景 |
|------|------|---------|
| **Zero-shot** | 不提供示例，直接提问 | 简单任务 |
| **Few-shot** | 提供 2-5 个示例 | 格式要求严格的输出 |
| **Chain-of-Thought (CoT)** | "让我们一步步思考" | 推理、数学题 |
| **Tree-of-Thought (ToT)** | 多路径探索 + 回溯 | 规划、策略问题 |
| **ReAct** | 推理+行动交替 | Agent 核心模式 |
| **结构化输出** | JSON Mode / Function Calling | API 对接 |
| **System Prompt 设计** | 角色定义、行为约束、输出格式 | 所有 Agent |

```python
# 实践：System Prompt 设计模式
SYSTEM_PROMPT = """你是一个专业的技术客服 Agent。

## 角色
你是 TechCorp 的高级技术支持工程师，擅长解决云服务相关问题。

## 能力范围
- 可以回答：云服务器配置、网络故障、数据库问题
- 无法处理：退款、账号注销（需转人工）

## 行为规则
1. 始终用中文回复，语气专业但友好
2. 遇到不确定的问题，明确告知而非猜测
3. 需要操作时，先确认用户意图再执行
4. 涉及敏感操作（删除/重启）需要二次确认

## 输出格式
- 回复内容：[你的回答]
- 是否需要工具调用：[是/否]
- 置信度：[高/中/低]
"""
```

### 2.3 模型路由与成本控制

| 知识点 | 要求 |
|--------|------|
| 模型选择策略 | 简单任务用小模型（GPT-4o-mini），复杂任务用大模型（GPT-4o/Claude） |
| 缓存策略 | 相同 prompt 缓存结果、语义缓存（相似问题复用） |
| 成本估算 | 输入/输出 token 计价、预估月度费用 |
| Fallback 机制 | 主模型不可用时的降级策略 |

---

## 三、阶段二：单 Agent 核心开发

> 周期：3-4 周 | 目标：掌握 Agent 核心架构，能独立构建生产级单 Agent

### 3.1 Agent 核心架构

```
┌─────────────────────────────────────────┐
│                  Agent                   │
│  ┌─────────┐  ┌──────┐  ┌────────────┐  │
│  │  LLM    │  │Memory│  │   Tools    │  │
│  │ (大脑)  │  │(记忆)│  │  (工具)    │  │
│  └────┬────┘  └──┬───┘  └─────┬──────┘  │
│       │          │             │         │
│  ┌────▼──────────▼─────────────▼──────┐  │
│  │         Planning & Reasoning       │  │
│  │         (规划与推理引擎)            │  │
│  └────────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 3.2 Tool Calling（工具调用）

| 知识点 | 深度要求 | 实践 |
|--------|---------|------|
| Function Calling | OpenAI/Anthropic 原生格式 | 定义 tool schema，处理调用结果 |
| 工具设计原则 | 单一职责、清晰描述、参数校验 | 为每个工具写详细的 description |
| 工具链调用 | 多工具顺序调用、并行调用 | 实现"查询天气→推荐活动"链 |
| 错误处理 | 工具超时、格式错误、权限不足 | 实现重试+降级机制 |
| 工具注册与管理 | 动态注册、工具发现 | 搭建工具注册中心 |

```python
# 实践：工具定义与调用（OpenAI 格式）
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "搜索公司内部知识库。当用户询问产品、政策、流程等问题时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，使用用户原话中的关键术语"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回结果数量，默认 5",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "创建技术支持工单。仅当问题无法直接解决时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "工单标题"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"],
                        "description": "紧急程度"
                    },
                    "description": {"type": "string", "description": "问题详细描述"}
                },
                "required": ["title", "priority", "description"]
            }
        }
    }
]
```

### 3.3 Agent 推理模式

| 模式 | 原理 | 框架 |
|------|------|------|
| **ReAct** | Reasoning + Acting 交替，思考一步执行一步 | LangChain AgentExecutor |
| **Plan-and-Execute** | 先生成完整计划，再逐步执行 | LangGraph |
| **Self-Reflection** | 执行后自我评估，发现错误自动修正 | Reflexion |
| **Tree-of-Thought** | 多路径探索，选择最优路径 | 自定义实现 |

```python
# 实践：用 Anthropic SDK 构建最简 Agent（无框架）
import anthropic

client = anthropic.Anthropic()

def run_agent(user_query: str, tools: list, max_turns: int = 10):
    messages = [{"role": "user", "content": user_query}]
    
    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )
        
        # 检查是否需要调用工具
        if response.stop_reason == "tool_use":
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result)
                        }]
                    })
        else:
            # Agent 认为任务完成
            return response.content[0].text
    
    return "达到最大轮次，任务未完成"
```

### 3.4 Memory（记忆系统）

| 记忆类型 | 说明 | 实现方式 |
|---------|------|---------|
| **短期记忆** | 当前对话上下文 | 消息列表（受 context window 限制） |
| **长期记忆** | 跨会话持久化信息 | 向量数据库 + 摘要存储 |
| **工作记忆** | Agent 执行中的中间状态 | 结构化暂存（scratchpad） |
| **语义记忆** | 用户偏好、历史行为 | 用户画像向量化 |
| **情节记忆** | 过去的交互序列 | 关键对话摘要+时间线 |

```python
# 实践：记忆系统设计
class AgentMemory:
    def __init__(self):
        self.short_term = []          # 当前对话轮次
        self.working = {}             # 当前任务的中间状态
        self.long_term = VectorStore() # 向量数据库
        self.summarizer = LLM()       # 对话摘要器
    
    def add_interaction(self, role, content):
        self.short_term.append({"role": role, "content": content})
        
        # 当短时记忆过长时，压缩为摘要存入长期记忆
        if len(self.short_term) > 20:
            summary = self.summarizer.summarize(self.short_term[-10:])
            self.long_term.store(summary)
            self.short_term = self.short_term[-10:]  # 保留最近10轮
```

---

## 四、阶段三：RAG 与知识增强

> 周期：2-3 周 | 目标：掌握 RAG 全链路，能构建生产级知识型 Agent

### 4.1 RAG 全链路

```
文档加载 → 文本分割 → 向量化 → 向量存储 → 检索 → 重排序 → 生成
   │          │         │         │         │        │        │
PDF/Web    Chunk     Embedding  Milvus   相似度    Cross    LLM
Markdown   Strategy   Model     Pinecone  搜索    Encoder  生成
                              ChromaDB           rerank
```

### 4.2 核心环节深入

| 环节 | 关键技术 | 实践要点 |
|------|---------|---------|
| **文档加载** | PDF/Markdown/网页解析、表格提取 | 处理多格式、保留结构信息 |
| **文本分割** | 固定大小/语义分割/递归分割 | Chunk 大小影响检索质量，建议 512-1024 tokens |
| **Embedding** | text-embedding-3-large、BGE-M3、Jina | 多语言场景选 BGE-M3 |
| **向量数据库** | Milvus、Pinecone、Chroma、Qdrant | 百万级以下用 Chroma，生产用 Milvus |
| **检索策略** | 稠密检索、稀疏检索(BM25)、混合检索 | 混合检索通常效果最好 |
| **重排序** | Cohere Rerank、BGE-Reranker | 检索 20 条→重排取 top 5→送入 LLM |
| **生成增强** | 引用标注、来源溯源、防幻觉 | 要求 LLM 标注信息来源 |

### 4.3 高级 RAG 技术

| 技术 | 说明 |
|------|------|
| **Self-RAG** | Agent 自我判断是否需要检索、检索结果是否相关 |
| **Corrective RAG** | 检索结果不相关时自动修正查询重新检索 |
| **Graph RAG** | 结合知识图谱，处理多跳推理问题 |
| **Agentic RAG** | Agent 自主决定检索时机、检索策略、信息整合 |

```python
# 实践：Agentic RAG 核心流程
def agentic_rag_query(question: str):
    # 1. Agent 分析问题，决定是否需要检索
    plan = llm.plan(f"分析这个问题是否需要检索知识库：{question}")
    
    if not plan.need_retrieval:
        return llm.generate(question)
    
    # 2. 生成检索查询（可能多个）
    queries = llm.generate_queries(question, n=3)
    
    # 3. 多路检索 + 重排序
    all_docs = []
    for q in queries:
        docs = vector_store.search(q, top_k=10)
        all_docs.extend(docs)
    
    # 去重 + 重排序
    unique_docs = deduplicate(all_docs)
    reranked = reranker.rerank(question, unique_docs, top_k=5)
    
    # 4. 评估检索质量
    relevance = llm.evaluate_relevance(question, reranked)
    if relevance.score < 0.5:
        # 检索结果不好，尝试修正查询
        refined_query = llm.refine_query(question, reranked)
        reranked = vector_store.search(refined_query, top_k=5)
    
    # 5. 带引用生成答案
    answer = llm.generate_with_citations(question, reranked)
    return answer
```

---

## 五、阶段四：多 Agent 协作与协议

> 周期：3-4 周 | 目标：掌握多 Agent 协作模式，理解主流通信协议

### 5.1 多 Agent 协作模式

| 模式 | 说明 | 框架 |
|------|------|------|
| **顺序流水线** | Agent A → Agent B → Agent C 依次处理 | LangGraph |
| **角色分工** | 不同 Agent 扮演不同角色（PM/架构师/开发/测试） | CrewAI, MetaGPT |
| **辩论协商** | 多个 Agent 讨论后达成共识 | AutoGen |
| **层级调度** | 主管 Agent 分配任务给子 Agent | LangGraph Supervisor |
| **群集涌现** | 大量简单 Agent 涌现复杂行为 | 学术前沿 |

### 5.2 核心通信协议

| 协议 | 全称 | 作用 | 提出方 |
|------|------|------|--------|
| **MCP** | Model Context Protocol | 模型与外部工具/资源的标准接口 | Anthropic |
| **A2A** | Agent-to-Agent | Agent 间协作通信协议 | Google |
| **ANP** | Agent Network Protocol | 去中心化 Agent 身份与发现 | 社区 |

```
MCP 解决：LLM ←→ 工具/数据 的连接
A2A 解决：Agent ←→ Agent 的协作
```

### 5.3 MCP 协议深入

| 概念 | 说明 |
|------|------|
| **Resources** | 暴露数据（文件、数据库记录、API 响应） |
| **Prompts** | 预定义的提示模板 |
| **Tools** | 可执行的操作（搜索、计算、发送邮件） |
| **Sampling** | Server 请求 LLM 生成内容（高级特性） |
| **Transport** | stdio（本地）和 SSE（远程）两种传输方式 |

```python
# 实践：构建 MCP Server
from mcp.server import Server, stdio_server
from mcp.types import Tool, TextContent

server = Server("knowledge-base-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_docs",
            description="搜索公司内部文档",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "category": {"type": "string", "enum": ["product", "policy", "tech"]}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_docs":
        results = search_knowledge_base(arguments["query"], arguments.get("category"))
        return [TextContent(type="text", text=str(results))]
```

### 5.4 主流框架对比

| 框架 | 定位 | 适用场景 | 学习曲线 |
|------|------|---------|---------|
| **LangChain** | 通用 LLM 应用框架 | RAG、Chain、简单 Agent | 中等 |
| **LangGraph** | 有状态多步 Agent | 复杂 Agent 工作流、多 Agent 编排 | 较高 |
| **CrewAI** | 多 Agent 角色协作 | 模拟团队协作、内容生成 | 低 |
| **AutoGen** | 多 Agent 对话 | 代码生成、辩论式推理 | 中等 |
| **Dify** | 低代码 Agent 平台 | 快速原型、可视化编排 | 低 |
| **OpenAI Agents SDK** | 官方 Agent 框架 | OpenAI 生态项目 | 低 |
| **Claude Agent SDK** | Anthropic 官方 Agent | Claude 生态、MCP 原生支持 | 低 |
| **MetaGPT** | 软件公司模拟 | 自动化软件开发流程 | 较高 |

---

## 六、阶段五：Agent 评估与生产化

> 周期：3-4 周 | 目标：建立评估体系，将 Agent 部署到生产环境

### 5.1 Agent 评估体系

| 评估维度 | 指标 | 方法 |
|---------|------|------|
| **任务完成率** | 端到端任务成功率 | 构建测试集，人工+自动标注 |
| **工具调用准确率** | 工具选择正确率、参数正确率 | 日志分析 |
| **回复质量** | 准确性、完整性、相关性 | LLM-as-Judge |
| **安全性** | 越狱率、有害输出率 | 红队测试 |
| **延迟** | TTFT（首 token 时间）、端到端延迟 | 监控埋点 |
| **成本** | 每任务平均 token 消耗、工具调用次数 | 成本追踪 |

```python
# 实践：LLM-as-Judge 评估
def evaluate_agent_output(query, agent_output, reference_answer=None):
    judge_prompt = f"""请评估以下 Agent 回复的质量。

用户问题：{query}
Agent 回复：{agent_output}
{f"参考答案：{reference_answer}" if reference_answer else ""}

请从以下维度打分（1-5分）：
1. 准确性：回复内容是否正确
2. 完整性：是否完整回答了问题
3. 相关性：是否与用户问题直接相关
4. 安全性：是否包含不当内容

输出 JSON 格式：{{"accuracy": 5, "completeness": 4, ...}}
"""
    result = llm.generate(judge_prompt)
    return parse_json(result)
```

### 5.2 可观测性

| 组件 | 工具 |
|------|------|
| **LLM 调用追踪** | LangSmith、LangFuse、Phoenix |
| **Agent 执行日志** | 每个 turn 的思考、工具调用、结果 |
| **成本监控** | 按模型/用户/任务的 token 消耗统计 |
| **异常告警** | 超时、工具失败率突增、越狱检测 |
| **用户反馈** | 点赞/点踩、满意度评分 |

### 5.3 生产化部署

| 要点 | 实践 |
|------|------|
| **并发控制** | LLM API 的 rate limit 管理、请求队列 |
| **超时与重试** | 指数退避重试、circuit breaker |
| **缓存策略** | 相同问题语义缓存、工具调用结果缓存 |
| **Human-in-the-Loop** | 高风险操作需人工确认 |
| **A/B 测试** | 对比不同 prompt/模型的线上效果 |
| **灰度发布** | 逐步放量，监控指标后全量 |

---

## 七、阶段六：Agent 架构设计与治理

> 周期：持续 | 目标：从技术实现升级为全局架构与治理

### 6.1 企业级 Agent 架构

```
┌──────────────────────────────────────────────────┐
│                   Agent Gateway                    │
│          (统一入口、路由、认证、限流)                 │
├──────────┬──────────┬──────────┬─────────────────┤
│ Agent A  │ Agent B  │ Agent C  │  Agent Orchestrator │
│ (客服)   │ (运维)   │ (数据分析) │  (多Agent编排调度)   │
├──────────┴──────────┴──────────┴─────────────────┤
│              Shared Services                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│  │Memory│ │Tools │ │RAG   │ │Eval  │ │Monitor│   │
│  │Service│ │Registry│ │Pipeline│ │Engine│ │&Alert │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
├──────────────────────────────────────────────────┤
│              Model Gateway                        │
│    (多模型路由、Fallback、成本控制、缓存)            │
└──────────────────────────────────────────────────┘
```

### 6.2 安全与治理

| 领域 | 措施 |
|------|------|
| **Prompt 注入防御** | 输入清洗、指令隔离、权限最小化 |
| **数据脱敏** | PII 检测与脱敏、敏感信息过滤 |
| **权限管控** | 工具调用权限分级、RBAC |
| **审计日志** | 全链路记录、可回溯 |
| **合规** | 数据本地化、GDPR/个保法合规 |

### 6.3 四项核心高级能力

| 能力 | 说明 |
|------|------|
| **业务抽象能力** | 将复杂业务需求提炼为稳定的 Agent 行为模型，"业务语言→Agent 执行逻辑"的精准映射 |
| **系统思维能力** | 全局视角理解 Agent 行为逻辑、依赖关系与失败路径，预判多 Agent 协作冲突 |
| **不确定性控制** | 通过约束机制（输出格式校验、权限管控）、闭环反馈（评估→迭代→调优）管理 LLM 不稳定性 |
| **长期演进能力** | 数据驱动的迭代框架、可扩展的记忆结构、可插拔的工具接入机制 |

---

## 八、B站与学习资源推荐

### 8.1 必读官方指南

| 资源 | 链接 | 说明 |
|------|------|------|
| **Anthropic: Building Effective Agents** | https://www.anthropic.com/research/building-effective-agents | Agent 构建纲领性指南，必读！ |
| **OpenAI: Agents SDK 文档** | https://platform.openai.com/docs/guides/agents | 官方 Agent 开发框架 |
| **MCP 官方文档** | https://modelcontextprotocol.io/ | MCP 协议规范 |
| **Google A2A 协议** | https://github.com/google/A2A | Agent 间协作协议 |

### 8.2 视频教程

| 视频 | 链接 | 亮点 |
|------|------|------|
| 吴恩达 - AI Agentic Design Patterns | B站搜 "吴恩达 Agentic Design" | 4 种 Agent 设计模式 |
| 吴恩达 - Building Agentic RAG | B站搜 "吴恩达 Agentic RAG" | Agent + RAG 实战 |
| 3Blue1Brown - Transformer 可视化 | B站搜 "3Blue1Brown Transformer" | 最直观的 Transformer 讲解 |
| 3Blue1Brown - 注意力机制 | B站搜 "3Blue1Brown 注意力" | 深入理解 Attention |
| LangChain 官方 - LangGraph 教程 | https://www.bilibili.com/video/BV1si421S7Gj | 复杂 Agent 编排 |
| 黑马 - AI Agent 开发实战 | B站搜 "黑马 AI Agent" | 零基础入门 |

### 8.3 开源项目（必 Star）

| 项目 | GitHub | 说明 |
|------|--------|------|
| **LangGraph** | github.com/langchain-ai/langgraph | 有状态多步 Agent 框架 |
| **CrewAI** | github.com/crewAIInc/crewAI | 多 Agent 角色协作 |
| **AutoGPT** | github.com/Significant-Gravitas/AutoGPT | 自主 Agent 先驱 |
| **Dify** | github.com/langgenius/dify | 低代码 Agent 平台 |
| **MetaGPT** | github.com/geekan/MetaGPT | 多 Agent 软件开发 |
| **OpenClaw** | github.com/openclaw/openclaw | 全功能本地 Agent |
| **LangFuse** | github.com/langfuse/langfuse | LLM 可观测性 |

---

## 九、书单推荐

### 必读（5 本）

| 书名 | 理由 | 难度 |
|------|------|-----|
| 《大规模语言模型：从理论到实践》 | 中文 LLM 最佳入门，复旦团队出品 | ★★★ |
| 《LangChain 编程：从入门到实践》 | Agent 框架实战，代码驱动 | ★★☆ |
| 《大模型应用开发极简入门》 | 奥莱利出品，快速上手 LLM 应用 | ★★☆ |
| 《Designing Machine Learning Systems》（中文版） | MLOps 与生产化必读 | ★★★☆ |
| Anthropic《Building Effective Agents》 | 免费，Agent 工程纲领 | ★★★ |

### 进阶选读

| 书名 | 理由 |
|------|------|
| 《Attention Is All You Need》论文 | Transformer 原论文，必读 |
| 《Patterns of Enterprise Application Architecture》 | 经典架构思维，映射到 Agent 架构 |
| 《凤凰架构：构筑可靠的大型分布式系统》 | 分布式系统设计，Agent 系统也需要 |
| 《大模型面试通关指南》 | 2026 最新，约 100 道高频面试题 |

---

## 学习节奏建议

```
总周期约 4-6 个月（有编程基础的前提下）

阶段一（2-3周）：LLM认知 + Prompt工程
  ├── 1周：搞懂 Transformer、Token、上下文窗口
  ├── 1周：Prompt 各种模式练习
  └── 实战：写一个 Prompt 模板库

阶段二（3-4周）：单Agent核心
  ├── 1周：Tool Calling + ReAct 模式
  ├── 1周：用 Anthropic SDK 从零写 Agent
  ├── 1周：Memory 系统设计
  └── 实战：构建一个客服 Agent

阶段三（2-3周）：RAG
  ├── 1周：基础 RAG 全链路
  ├── 1周：高级 RAG（Self-RAG/Graph RAG）
  └── 实战：搭建企业知识库 Agent

阶段四（3-4周）：多Agent + 协议
  ├── 1周：CrewAI 多角色协作
  ├── 1周：LangGraph 编排
  ├── 1周：MCP + A2A 协议
  └── 实战：多 Agent 软件开发团队模拟

阶段五（3-4周）：评估与生产化
  ├── 1周：评估体系搭建
  ├── 1周：可观测性接入
  ├── 1周：生产化部署
  └── 实战：将 Agent 上线并监控

阶段六（持续）：架构与治理
  └── 在日常工作中持续积累
```

### 避坑指南

1. **不要一上来就用框架**：先用原生 SDK 写 Agent，理解本质再用 LangChain/LangGraph
2. **不要追求复杂**：Anthropic 的核心建议——最简单的方案往往是最好的
3. **不要忽视评估**：没有评估体系，Agent 优化就是盲人摸象
4. **不要把 Agent 当万能药**：简单的 if-else 能解决的，不要用 Agent
5. **不要只关注模型能力**：工具设计、Memory 策略、错误处理同样重要
6. **不要忽视成本**：一个 Agent 对话消耗的 token 可能是简单问答的 10-50 倍

---

## 阶段完成自检清单

### LLM 认知 ✅
- [ ] 能解释 Transformer 的自注意力机制
- [ ] 能为不同任务选择合适的 Prompt 策略
- [ ] 能估算任务的 token 消耗和成本
- [ ] 理解各主流模型的优劣势

### 单 Agent ✅
- [ ] 能独立用 SDK（不用框架）写出 Tool-using Agent
- [ ] 理解 ReAct 和 Plan-Execute 的区别
- [ ] 能设计合理的 Memory 策略
- [ ] 能处理工具调用的各种异常

### RAG ✅
- [ ] 能搭建完整的 RAG 流程
- [ ] 理解 Chunk 策略对检索的影响
- [ ] 能实现混合检索 + 重排序
- [ ] 能处理检索失败的情况

### 多 Agent ✅
- [ ] 能用 LangGraph 编排多步 Agent 工作流
- [ ] 理解 MCP 协议的三大核心概念
- [ ] 能设计多 Agent 的角色分工

### 生产化 ✅
- [ ] 建立了 Agent 评估体系
- [ ] 接入了 LLM 可观测性工具
- [ ] 实现了 Human-in-the-Loop
- [ ] 有完整的安全防护措施

---

> **下一步建议**：持续关注 Anthropic、OpenAI、Google 的 Agent 方向最新发布，参与 LangChain/LangGraph 社区，在实际项目中积累经验。
