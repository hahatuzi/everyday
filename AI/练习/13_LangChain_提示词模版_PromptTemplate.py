from langchain_core.prompts import PromptTemplete
from langchain_cmmunity.llms.tongyi import Tongyi

  prompt_template = PromptTemplate.from_template("我的邻居姓{lastname},刚生了个{gender},帮忙起个名字吧")
  prompt_text = prompt_template.format(name='章',gender="女儿")

  model = Tongyi(model="qwen-max")
  res = model.invoke(input=prompt_text)

  print(res)