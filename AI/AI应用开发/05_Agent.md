## 目录

1. [一、Agent智能体](#一、Agent智能体)
2. [Embedding向量化](#二、LangChain调用大模型)
3. [LangChain的提示词模版PromptTemplate类](#三、LangChain的提示词模版PromptTemplate类)
4. [Runnable知识点](#四、Runnable知识点)
5. [LangChain的临时记忆和长期会话记忆](#五、LangChain的临时记忆和长期会话记忆)
6. [基于LangChain的典型的RAG流程](#六、基于LangChain的典型的RAG流程)

---
## 一、Agent智能体
  ### 1.1 AI Agetn四大组件
  > Agent = **LLM** (大脑) + **Planning** (规划) + **Tool use** (执行) + **Memory** (记忆)。
  - 大脑LLM：负责推理，理解需求，拆解任务，判断对错
  - 记忆系统：短期会话记忆 + 长期向量记忆(记住你的偏好，历史任务经验)
  - Tools工具：能够根据需求去查谷歌搜索、读数据库、甚至跑 Python 代码。软件API,操作系统操作权限
  - 反思循环引擎Planning：能够将复杂的目标（如"帮我策划一场技术沙龙"）拆解成可执行的步骤，最重要的是让LLM具备**子任务拆解**和**反思**能力，让它形成思维树和思维链。评估执行结果，失败自动重试，调整方案
  ### 1.2 传统Chat Model对话模型 VS AI Agent智能体
  - AIAgent支持跨天跨系统，ChatModel仅支持单轮短流程简单文案
  - AIAgetn包括三层记忆：短期记忆，工作记忆，长期向量记忆，ChatModel仅当前会话短期上下文
  - AIAgent闭环循环**ReAct**:思考→行动→观察→再思考。LangChain的createAgent创建的Agent就是ReAct.ChatModel单向线性：输入→推理→输出，对话终止
  ### 1.3 AI Agent发展现状
  - copilot,Cursor,langChain,LlamaInex
  - 钉钉AI智能体
  ### 1.4 记忆系统
  - (1)瞬时记忆：仅保存当前一轮对话上下人，随着会话结束清空
  - (2)短期记忆：单次完整任务内的全部步骤：比如一次写方案，一次数据分析全过程
  - (3)长期记忆：用户历史任务
  - (4)技能记忆(工具记忆)
  ### 1.5 middleware中间件
  > 中间件的作用是对智能体额每一步工作进行控制和自定义的执行，作用包括：日志分析，提示词转换，工具选择，重试、备用、提前终止等逻辑操作，安全防护，个人身份检测等
  request → **before_agent** → **before_model** → **wrap_model_call** → model → **wrap_tool_call** → **after_model** → **after_agent** → result
  #### 节点式钩子
  - **before_agent**:agent执行之前拦截
  - **after_agent**:agent执行之后拦截
  - **before_model**:模型执行之前拦截
  - **after_model**:模型执行之后拦截
  #### 针对工具和模型的包装式钩子
  - **wrap_model_call**:每个模型调用时拦截
  - **wrap_tool_call**:每个工具调用时拦截
  ```py
    from json import tool
    from langchain.agents import AgentState
    from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
        wrap_tool_call


    @tool(description="查询天气")
    def get_weather() -> str:
        return "晴天"

    @before_agent
    def log_before_agent(state:AgentState, runtime) -> None:
        print(f"[before_agent{len(state['messages'])}")

    @after_agent
    def log_after_agent(state:AgentState, runtime) -> None:
        print(f"[after_agent{len(state['messages'])}")
    @before_model
    def log_before_model(state:AgentState, runtime) -> None:
        print(f"[before_model{len(state['messages'])}")
    @after_model
    def log_after_model(state:AgentState, runtime) -> None:
        print(f"[after_model{len(state['messages'])}")
    @wrap_model_call
    def model_call_hook(request, handler):
        print("模型调用了")
        return handler(request)
    @wrap_tool_call
    def tool_call_hook(request, handler):
        print(f"工具执行:{request.tool_call['name']}")
  ```
## 二、AI Agent

  ### 2.1 AI Agent增强的方法
  > 普通的 LLM 只是 One-shot（一次性） 的响应，而 Agent 的核心在于 Iterative（迭代）。ReAct 模式 (Reason + Act) 是目前最主流的 Agent 推理逻辑，它通过**推理**和**行动**来增强推理和决策的效果
  - 1.Thought (思考)： 模型描述当前要做什么，为什么要这么做。
  - 2.Action (行动)： 模型选择一个工具（如：Google Search）。
  - 3.Observation (观察)： 模型读取工具返回的结果。
  - 4.Repeat (循环)： 重复上述步骤，直到得出最终答案。
---
  ### 2.2 规划模块是如何把复杂任务拆成步骤的？依靠了什么技术
  - **CoT思维树**：按照顺序执行，比如：安排出游→查景点→找餐厅→规划线路→整理清单
  - **ToT思维树**：多方案对比，择优选择
---
  ### 2.3 任务规划能力
  - 链式思考
  - 任务拆解：比如
  - 优先级排序
  - 任务合并与收尾
  ### 2.5 Agent认知框架
  - plan-and-execute
----

---
  ### 2.7 如何选择相关技术
  测试数据-->用对话应用验证可行性-->是否要补充知识-->是否要对接其他系统-->是否需要尝试微调-->交付
                                                  -->RAG               -->Function Calling-->用历史数据做Fine-tuning
---
  ### 2.8 旅游规划案例：
  - 大脑中枢：规划行程的你
  - 规划：步骤1：规划打车路线，步骤2：订饭店，酒店。。。
  - 调用工具：调用MCP或者FunctionCalling等API,滴滴打车，携程，美团订酒店
  - 记忆能力：沟通时，要知道上下文。比如订酒店要知道是哪里的酒店，不能聊着聊着就忘记了最初的目的
  - 能够执行上述操作。
---
## 三、Agent的API
  - model
  - tool
  - system_prompt
  - response_format
  ### 3.1 Agent中传入模型的两种方式
  - (1)传入模型字符串：model = "deepseek-v4-flash"
  - (2)传入模型实例：
  ```js
    from langchain.chat_models import init_chat_model
    model = init_chat_model(model='deepseek-v4-pro')
  ```
  ### 3.2 Agent的输入，输出以及stream流式输出
  ### 3.3 Agent的tool以及工具调用流程
  > 用户提问 HumanMessage → AI分析是否需要调用工具 → 执行工具 → AI查看工具调用结果
  ### 3.4 agent的name和system_prompt
  - system_prompt:系统提示词，string,或者systemMessage,提示词设置方式包括**静态设置**和**动态设置**两种，动态设置需要中间件的参与
  ```js
    web_search = TavilySearch(max_result = 5)
    
    agent = create_agent(
        model="deepseek-v4-pro",
        tool = [web_search],
        system_prompt = "你是一名多才多艺的智能助手，可以调用工具帮助用户解决问题",
        system_prompt = SystemMessage(
            "你是一个天气助手。",
            "当工具返回以'TEMP_UNAVAILABLE:'开头的时候，",
            "说明是临时故障，不要立即放弃,",
            "你应该再次调用同一个工具，最多重试3次，",
            "如果3次之后仍然失败，再向用户说明服务暂时不可用"
        )
    )
    result = agent.invoke({
        "messages":[
            {"role":"user", "content": "请帮助我查询2026年足球世界杯举办国家"}
        ]
    })
  ```
  ### 3.5 agent的结构化输出的四种策略
  - 方式一：**ProviderStrategy**，Pydantic结构化方式，ProviderStrategy是模型提供商的原生结构化输出结构
  ```py
    class ContractInfo(BaseModel):
        name:str = Field(description = "用户的姓名")
        email:str = Field(description="用户的邮箱")
    agent = create_agent(
        model="",
        response_format: ProviderStrategy(ContractInfo)
    )
  ```
  - 方式二：**ToolStrategy**,对于不支持原生结构化输出的模型，LangChain采用ToolStrategy来结构化输出
  - 方式三：**AutoStrategy**，langchain将我们传入的类型自动转化为AutoStrategy类型，触发自动选择策略
  - 方式四：**None**,不提供任何配置
  ### 3.6 ToolStrategy中的三个配置参数
  - **schema**：必需，与模型提供商的schema参数功能一致，支持**Pydantic，TypeDict,JSON Schema,dataclass**
  - **tool_message_content**:可选，用于自定义生成结构化输出时，会话历史的提示信息
  - **handle_errors**:可选，错误处理机制，用于指定数据校验失败时的重试策略
  ### 3.7 agent的流式输出
  > agetn.stream(stream_mode=指定模式)，stream_mode包括values,updates,messages,custom,checkpoints,task,debug。默认的模式是updates
  - (1)**stream_mode=values**,每个步骤执行后都会输出完整的状态信息，适合每一步都需要完整状态的场景
  - (2)**stream_mode=updates**,
  - (3)**stream_mode=messages**,会返回token相关的元数据，实现打字机的效果
  - (4)**stream_mode=tasks**,
  - (5)**stream_mode=debug**,输出模式
  - (6)**stream_mode=checkpoints**,每当检查点被触发时，都会输出相关的状态信息
  - (7)**stream_mode=custom**,通过get_stream_write在工具或者节点内部自定义发送的数据
  ### 3.10 典型的LangChain的ReaAct案例
  > langchain.agent使用create_agent方法创建的就是一个Agent
  ``js
    from langchain.agents import create_agent
    from langchain_community.chat_models.tongyi import ChatTongyi
    from langchain_core.tools import tool

    from FewShot提示词模版 import model

    @tool
    def get_price(name:str) -> str:
        return f"股票{name}的价格是20元"
    @tool
    def get_info(name:str) -> str:
        return f"股票{name},是一家A股上市公司，专注于某某领域"

    agent = create_agent(
        model=ChatTongyi(model="qwen-max",api_key="sk-XXX"),
        tools = [get_price, get_info],
        system_prompt = "你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"
    )

    for chunk in agent.stream(
        {"messages":[{"role":"user", "content":"东方财富的股价多少，并介绍一下它"}]},
        stream_mode="values"
    ):
      latest_message = chunk["message"][-1]
      if latest_message.content:
          print(latest_message.content.strip())
    try:
        if latest_message.tool_calls:
            print(f"Calling tools:{[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass
  ```