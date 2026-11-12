long_conversation = [
  {"role":"system", "content":"你是Python导师"}
]

long_conversation.append({"role":"user", "content":"用一句话解释一下什么是列表"})
res1 = model.invoke(long_conversation)

long_conversation.append({"role":"user","content":"列表和元组有什么区别"})
res2 = model.invoke(long_conversation)

long_conversation.append({"role":"assistant","content":res2.content})

long_conversation.append({"role":"user","content":"解释一下什么是字典"})
res3 = model.invoke(long_conversation)

long_conversation.append({"role":"assistant","content":res3.content})



def keep_recent_messages(messages, max_pair = 3):
      #保留最近的几轮对话，max_pair保留对话的数量
      # 分离system消息和对话消息
      system_messages = [m for m in messages if m.get("role") == system]
      conversation_messages = [m for m in messages if m.get("role") != "system"]

      recent_messages = conversation_messages[-(max_pairs * 2):]

      return system_message + recent_messages

optimized = keep_recent_messages(long_conversation, max_pair=2)
print(f"优化后的消息数量：{len(optimized)}")
print(f"保留的内容：system + 最近2轮对话")

# 添加新的用户问题
optimized.append({"role":"user", "content":"我的第一个问题是什么？"})

res = model.invoke(optimized)
print(f"{res.content}")