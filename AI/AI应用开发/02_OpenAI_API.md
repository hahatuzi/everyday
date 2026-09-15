## 一、OpenAI的API接口
  > pip install openai
  ### 1.1 OpenAI的两类API
  - Completion API:续写API
  - Chat API:多轮对话，但是可以用对话逻辑完成任何任务，包括续写文本
  ```python
    response = client.chat.completions.create(
      model,
      messages,
      temperature：1.5,// 生成结果的多样性，0~2之间，默认为1，越大越随机，越小越固定
      stream=True,// 数据流模式，一个字一个字地接收
      seed=None,// 随机数种子，指定具体指后
      top_p = 1, // 随机采样时，只考虑概率前百分之几的token
      n =1,, // 一次返回n条结果
      max_tokens = 100, // 每条结果最多几个token,超过截断
      presence_penalty = 0, // 对出现过的token的概率进行降权
      frequency_penalty = 0, // 对出现过的token根据其出现过的频率
      logit_bias = {}, // 对指定token的采样概率手工加权
    )
  ```
---
  ### 1.2 message：对象数组，提供给模型的消息
    - role属性
      - user:用户，向LLM提问
      - system：系统，用户对LLM的要求
      - assitant:AI助手，LLM给出的回复
    - content属性
  ### 1.3 OpenAI的流式输出和非流式输出
    ```python
      # 非流式输出
      print(response.choices[0].message.content, end = '|')
      # 流式输出
      for chunk in response:
        print(chunk.choices[0].delta.content)
    ```
---
  ### 1.4 案例
  ```python
    import os
    from openai import OpenAI

    client = OpenAI(
        api_key= 'sk-XXX',
        base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
      model="deepseek-v4-pro",
      messages=[
          {"role": "user", "content": "你是谁？"},
          {"role":"system","content":"回答不要超过十个字"}
      ],
      temperature：1.5,
       stream=True
    )
  ```
---
## 二、工具
  ### 2.1 使用步骤：
  - 确定LLM
  - 定义工具函数
  - 描述函数
  - 封装LLM
  - 调用LLM

---
## 三、记忆机制与对话管理
  > 将完整的对话记录下来，让LLM知道上次调用的结果，形成上下文记忆，但是内容特别长的时候会导致开销增加，甚至超过上下文限制，导致调用失败
  ### 3.1 上下文长度计算
  > pip install deepseek_tokenizer
  ```python
    from deepseek_tokenizer import ds_token
    result = ds_token.encode('你是谁？')
    print(result,f"token数:{len(result)}")
    # 统计message_history
    def token_by_messages(message_history:list):
      tokens = 0
      for msg in message_history:
        text= msg['content']
        tokens += len(ds_token.encode(text))
      return tokens
  ```
---
  ### 3.2 滑动窗口
  >对message_history进行裁剪，仅保留system,和最新的k个user提示
  ```python
    def context_sliding_window(message_list:list,k = 2):
      new_message_list:list = message_list[-1*k:]
      # 如果丢失了系统提示，就手动补充上
      if new_message_list[0]['role'] != 'system':
        if message_list[0]['role'] == 'system':
          new_message_list.insert(0,message_list[0])
      return new_message_list
    print(context_sliding_window(message_history))
  ```
---
  ### 3.3 摘要总结
  > 利用LLM的摘要总结能力，总结此前对话，并替代完整的对话
  ```python
    def context_summary(message_list):
      response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
          {"role":"user","content":f"请对如下对话进行总结：{message_list}"}
        ]
      )
      new_message_list = [{"role":"system","context":f"请对此前对话进行总结：{response.choices[0].message.content}"}]
      return new_message_list
    print(context_summary(message_history))
  ```
  ### 3.4 其他记忆管理机制：
  - 知识图谱记忆
  - 向量数据库记忆

## 四、ReAct示例

# 五、多Agent编排
## 幻觉
  > 通俗：模型自信满满的**一本正经编造不存在的事实、人名、数据、文献**。
  > 模型不是故意骗你，它只是预测下一个字，看起来通顺，但是内容是假的
  常见幻觉场景：编造参考文献、编造统计数字、编造案例、编造历史细节。
  缓解方法：prompt 加上：**如果不知道就说不知道，不要编造信息，所有回答必须基于提供的材料**。