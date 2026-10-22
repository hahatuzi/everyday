from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model="qwen-max",api_key="sk-")
# prompt = PromptTemplate.from_template("你需要根据会话历史回应用户问题。对话历史:{chat_history}，用户提问：{input}，请回答")
chat_prompt = PromptTemplate.from_template([
    ("system","你需要根据会话历史回应用户问题，对话历史："),
    MessagesPlaceholder("chat_history"),
    ("human","请回答一下问题：{input}")
])
str_parser = StrOutputParser()

base_chain = chat_prompt | model | str_parser

store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }

    res = conversation_chain.invoke({"input":"小明有2只猫"},session_config)
    print("第1轮：",res)
    res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    print("第2轮：", res)
    res = conversation_chain.invoke({"input": "总共有几只宠物"}, session_config)
    print("第3轮：", res)