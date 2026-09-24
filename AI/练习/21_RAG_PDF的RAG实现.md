# 一：步骤
  ## 1.准备环境
  ```py
    import os
    import numpy as np
    import json
    import fitz
    import dashscope
    from openai import OpenAI
  ```
  ## 2.从PDF文件中提取文本
  ```py
    def extract_text_from_pdf(pdf_path):
      #打开PDF文件
      document = fitz.open(pdf_path)
      # 初始化一个空字符串存储提取出的文本
      all_text = ""
      #遍历PDF中的每一页
      for page_num in range(document.page_count):
          page = document[page_num] # 获取页面
          text = page.get_text("text") # 从页面提取文本
          all_text += text # 将提取出的文本追加到al1_text字符串
      return all_text # 返回提取出来的文本
  ```
  ## 3.对提取的文本进行分块
  ```py
    def chunk_text(text_input, chunk_size, overlap_size):
      text_chunks=[] #初始化一个列表存储文本块
      # 循环遍历文本，步长为(chunk_size - overlap_size)
      for i in range(0, len(text_input), chunk_size - overlap_size):
          text_chunks.append(text_input[i:i + chunk_size]) # 追加从i到i+chunk_size的文本块到text_chunks列表
      return text_chunks #返回文本块列表
  ```
  ## 4.设置opanAI API客户端
  ## 5.提取并分块PDF文件内容
  ## 6.创建文本块的嵌入向量
  ## 7.执行语义搜索
  ## 8.基于检索块生成响应
  ## 9.评估回答