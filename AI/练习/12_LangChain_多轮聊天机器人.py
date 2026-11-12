messages = [
  {"role":"system", "content":"你是Python导师,可以回答相关问题"}
]

def keep_recent_messages(messages, max_pair = 3):
      #保留最近的几轮对话，max_pair保留对话的数量
      # 分离system消息和对话消息
      system_messages = [m for m in messages if m.get("role") == "system"]
      conversation_messages = [m for m in messages if m.get("role") != "system"]

      recent_messages = conversation_messages[-(max_pair * 2):]

      return system_messages + recent_messages


i= 1 # i表示聊天轮次
while True:
      print("\n","="*10,f"第{i}轮对话开始","\n","="*10)
      user_input = input("请输入：")
      if user_input == "quit":
            print("会话已经接过，欢迎下次再来")
      messages.append({ "role":"user", "content":user_input })

      print("老师：",end="", flush = True)

      memory_messages = keep_recent_messages(messages, max_pairs = 5)
      for chunk in model.stream(memory_messages):
            if chunk.content:
                  print(chunk.content, end = '', flush=True)
                  reply_content = chunk.content

      print("\n","="*10,f"第{i}轮对话结束","\n","="*10)
      i += 1

      # 将模型的响应添加到消息列表
      messages.append({"role":"assistant","content":reply_content})

