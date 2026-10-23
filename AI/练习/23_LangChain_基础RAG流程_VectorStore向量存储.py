from langchain_chroma import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# vector_store = Chroma(
#     collection = "test",
# )
vector_store = InMemoryVectorStore(embedding = DashScopeEmbeddings())
loader = CSVLoader(
    path = "./test.csv",
    encoding = "utf-8",
    source_column= "source",
)

documents = loader.load()

vector_store.add(documents, ids=["id"+ str(i) for i in range(1,len(documents)+1) ])

vector_store.delete(["id1","id2"])
result = vector_store.similarity_search(
    "python是不是很简单"
)
print(result)