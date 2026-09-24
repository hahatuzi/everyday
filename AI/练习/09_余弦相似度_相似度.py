product_texts = [
  "商品1:智能手表,支持心率监测",
  "商品2:蓝牙耳机,降噪功能强大",
  "商品3:健身器材,多档调节",
  "商品4:游戏鼠标,灵敏度高",
  "商品5:办公椅,符合人体工学",
  "商品6:超高清显示器,支持HDR",
]

policy_texts = [
  "7天无理由退货",
  "超过7天但是商品无损坏可申请换货",
  "保修期内可以免费维修",
  "退货需要保持商品以及包装完好",
  "电子产品超过30太难仅提供维修服务",
  "特殊定制商品不支持退货"
]
("faiss_policy_index", embeddings, allow_dangerous_deseriablization = True)
query= "小米耳机坏了怎么办"
docs_product = product_db.similarity_search(query, k =2)
docs_policy = product_db.similarity_search(query, k =2)

all_docs = docs_product + docs_policy

context = "\n\n".join([doc.page_content for doc in all_docs])

print("\n===多库检索结果")
print(context)