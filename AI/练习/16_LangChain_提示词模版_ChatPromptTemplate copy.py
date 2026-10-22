from langchain_core.prompts import ChatPromptTemplate, MessagePlaceholder
from langchain_cmmunity.llms.tongyi import Tongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
  [
    ("system":"你是一个边塞诗人，可以作诗。"),
    MessagePlaceholder("history"),
    ("human","请再来一首唐诗")
  ]
)

history_data = [
  ("human","你来写一首唐诗"),
  ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
  ("human","再来一首"),
  ("ai",'')
]
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
model = Tongyi(model="qwen-max")
res = model.invoke(input=prompt_text)

print(res)