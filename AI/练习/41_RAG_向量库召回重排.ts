// 1. 用户query
const query = "NestJS依赖注入原理";

//  2. 召回：向量库召回Top20
const recallChunks = await vectorDb.search(query, {topK:20});

// 3. Rerank重排
const reranked = await reranker.rerank(query, recallChunks.map(c=>c.text));
//  排序+过滤，取top5
const topChunks = reranked
  .filter(item => item.score > 0.3)
  .sort((a,b)=>b.score - a.score)
  .slice(0,5);

//  4. 拼接参考文档
const context = topChunks.map(c=>c.text).join("\n---\n");

// 5. 送入LLM
const llmResp = await openai.chat.completions.create({
  model:"gpt-3.5-turbo",
  messages:[
    {role:"system", content:`基于下面文档回答问题，不知道就说不知道。\n参考文档：${context}`},
    {role:"user", content:query}
  ]
})
