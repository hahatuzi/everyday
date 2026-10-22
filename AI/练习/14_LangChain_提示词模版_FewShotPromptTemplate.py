from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
example_template = PromptTemplate.from_template("词语：{word},它的反义词是{antoym}")
example_data = [
  {"word":"大","antoym":"小"},
  {"word":"多","antoym":"少"},
]

few_shot_template = FewShotPromptTemplate(
  example_prompt = example_template,
  examples = example_data,
  prefix = "告知我词语的反义词，我提供如下示例：",
  suffix = "基于前面的实例告诉我，{input_word}的反义词是什么？",
  input_variables = ["input_word"]
)
prompt_text = few_shot_template.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)
model=Tongyi(model="qwen-max")
print(model.invoke(input=prompt_text))