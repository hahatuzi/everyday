from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms.tongyi import Tongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
  [
    SystemMessage("你是一个边塞诗人，可以作诗。"),
    MessagesPlaceholder("history"),
    ("human","请再来一首唐诗")
  ]
)

history_data = [
  ("human","你来写一首唐诗"),
  ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
  ("human","真棒，再来一首吧"),
  ("ai",'锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦')
]
# prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
# res = model.invoke(input=prompt_text)
model=Tongyi(model="qwen-max")

chain = chat_prompt_template | model

# res = chain.invoke({"history":history_data})
# print(res)

for chunk in chain.stream({"history":history_data}):
    print(chunk, end="",flush=True)