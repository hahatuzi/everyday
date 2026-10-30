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

## 三、Agent的API
  ### 3.1 Agent初体验
  ### 3.2 Agent的stream流式输出
  ### 3.3 典型的LangChain的ReaAct案例
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
        model=ChatTongyi(model="qwen-max",api_key="sk-16bb8531af8e41e5a78fef27c4079845"),
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