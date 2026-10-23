from langchain_community.document_loaders import TextLoader
  from langchain_text_splitters import RecursiveCharacterTextSplitter
  loader = TextLoader("./data/test.txt",encoding="utf-8")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
      chunk_size=500,#分段的最大字符数
      chunk_overlap=50,#分段之间允许重叠字符数
      separators=["\n\n","\n","。","!"]
    )
    split_docs = splitter.split_documents(docs)
    for doc in split_docs:
      print("="*20)
      print(doc)
      print("="*20)