from langchain_core.prompts import PromptTemplate
template = PromptTemplate.from_template("我的邻居是：{lastname},她喜欢{hobby}")
res = template.format(lastname="lisa", hobby="pop")
res2 = template.invoke({"lastname":"rose","hobby":"sing"})
print(res, type(res))
print(res2, type(res2))