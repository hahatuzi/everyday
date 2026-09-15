from agents import Agent,Runner
from agents.model_settings import ModelSettings
import local_settings
import asyncio

agent_A = Agent(name='AI助手',instructions='使用中文回答',model_settings=ModelSettings())
agent_B = Agent(name='AI助手',instructions='使用英文回答',model_settings=ModelSettings())
agent_C = Agent(name='AI助手',instructions='使用日文回答',model_settings=ModelSettings())

async def test():
    query = '你好'
    res1 = await Runner.run(agent_A,query)
    res2 = await Runner.run(agent_B,query)
    res3 = await Runner.run(agent_C,query)
    print(res1)
    print(res2)
    print(res3)

if __name__ == '__main__':
    asyncio.run(test())