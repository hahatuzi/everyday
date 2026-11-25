## 一、MCP简介
> MCP（model context Protocol）是由Anthropic退出的开放标准，用于便捷的将AI应用连接外部系统
### 1.1 三大概念。
- **MCP Servers**:提供获取并调用工具的接口：文件系统，数据库，API服务
- **AI应用、智能体**:
- **MCP协议层**：连接AI与外部能力的标准协议
### 1.2 MCP两大通信方式
- (1)stdio:通过标准输入输出进行进程之间的通信，比如Time MCP
- (2)Streamable Http:基于http的可流式通信方式,比如
## 1.3案例
  ```py
  from langchain_mcp_adapters.client imoprt MultiServerMcpClient
    client = MultiServerMcpClient(
      {
        "kiwi-com-flight-search":{
          "transport":"http",
          "url":"https://mcp.kiwi.com"
        },
        "time":{
          "transport":"stdio", # MCP的通信方式
          "command":"uvx",
          "args":[
            "mcp-server-time",
            "--local-timezone=Asia/Shanghai"
          ]
        }
      }
    )
    tools = await client.get_tools()
    agent = create_agent(model=model,tools=tools,system_prompt="你是一名旅行Agent。帮助用户找到最好的航班，不用追问用户问题。如果用户使用中文，则使用zh-cn作为区域设置值")
    response = await agent.ainvoke({
      "messages":[HumanMessage("查一下下周四从北京飞上海的航班")]
    })
    for message in response["messages"]:
      message.pretty_print()
  ```