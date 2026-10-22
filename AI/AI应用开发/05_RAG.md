## 目录

1. [RAG模型](#一、RAG模型)
2. [Embedding向量化](#二、Embedding向量化)
3. [RAG项目搭建](#三、RAG项目搭建)
4. [阶段三：LLM API 调用入门（2-3 周）](#四阶段三llm-api-调用入门)
5. [阶段四：Prompt 工程基础（2 周）](#五阶段四prompt-工程基础)
6. [阶段五：第一个 AI Agent（3-4 周）](#六阶段五第一个-ai-agent)
7. [阶段六：RAG 入门与项目实战（3-4 周）](#七阶段六rag-入门与项目实战)
8. [B站与学习资源推荐](#八b站与学习资源推荐)
9. [书单推荐](#九书单推荐)

---
## 一、RAG模型
  > RAG 核心流程：文档解析 → 分块 → 向量化 → 向量存储 → 检索 → 重排序 → 生成
  ### 1.1 核心原理
  - **第一步：离线阶段，知识库构建**，搭建一个知识库，支撑后面的检索
    - 知识库构建：收集文档，网页搜索资源等外部数据，一般解析成MD文档组成自己的数据库
    - 文档分块：固定大小chunk或者**语义切割**
    - 向量化处理：使用合适的Embedding Model模型将文本块转化为向量，并存储在向量数据库中
    - 向量存储：索引
  - **第二步：在线阶段，检索+生成**，找到合适的参考文档，检索方式的选择，整合提问和参考文档，提示词构建，大模型的选择
    - 查询处理
    - 重排序
    - 上下文组装：将搜索到的文本片段与用户的问题相结合，形成增强的上下文输入
    - 生成答案
----
  ### 1.2 实例步骤
  【文档入库】文档分片-->建立索引-->建立Embedding模型-->生成向量-->向量数据库
    ↓
  【用户问题】
    ↓
  【Query优化】（查询重写或者改写、扩展、多query）
    ↓
  【召回】向量检索 + BM25混合召回 → Top20候选chunk，向量数据库**召回**几个相关度最高的片段
    ↓
  【重排Rerank】reranker模型打分，重排、过滤 → Top5高质量上下文，生成相关度最高的片段
    ↓
  【把这5段文档拼入System Prompt】
    ↓
  【LLM基于参考文档回答，引用来源】

----
  ### 1.3 节点解析与文本分块
  #### (1)常见的分块策略
  - **固定长度分块**(固定长度，递归字符，按句分块)
  - **语义分块**(MarkDown,html),统一转换为MD文档，然后使用small 2 big转化。对话轮次语义/主题(向量相似度，LDA主题模型)
  - **层级分块**
  #### (2)分块参数
  - chunk_size:块大小，指单个Node允许的最大token数。块过大容易导致语义复杂，检索召回准确率下降。块过小会导致语义碎片化，单块信息不足
  - cunk_overlap:块重叠度，相邻两个分块头尾重复token数量，是解决上下文割裂的核心参数。
----
  ### 1.4 分阶段优化处理步骤：
  #### (1)Textloader非结构化文档的加载和处理
  - PDF解析text
    - OCR，视觉模型
    - 将pdf的每一页转换为图片
    - 阿里云现代智能文档技术
    - githb开源pdf解析引擎
  #### (2)TextSplitter文档切片
  - 固定长度分块
  - 语义分块
  - 层级分块

  #### (3)检索优化
  - RAG-Fusion:基于RRF算法对多个查询结果进行打分重排
  - 上下文增强检索：检索相关文档及上一个和下一个
  - CCH标题、摘要：为每一个chunk加上标题、摘要
  - 查询转换技术
    - (1)查询重写
    - (2)回退提问
    - (3)子查询拆解
  - 重排序ReRanking:对初步检索结果进行第二轮筛选，得到更精准的结果
    - 初步检索→文档评分→重新排序→内容选择
  #### (4)生成阶段
  - RAFT：对LLM进行RAG微调
  - 基于问题生成的RAG:为每一个chunk生成相关性的问题
  - 
----
  ### 1.6 向量
  ### 1.7 纯向量搜索的局限性：
  - 混合搜索：结合了BM25稀疏检索和向量检索稠密检索，通过langchain实现了代码展示了如何整合这两种检索方式。
  ### 1.8 余弦相似度
  > 在文本向量语义匹配中，余弦相似度是衡量两个向量方向相似程度的核心算法，即判断两段文本语义是否相似
  > 余弦相似度=两个向量的点积 ÷ 两个向量模长的乘积
---
## 二、Embedding向量化
  > Embedding向量就是一长串数字。比如[0.23,0.56,0.78]有多少个数字就是多少维。
  > 常见的embedding模型：openAIembeddings,ollamaEmbeddings,googleEmbedding
  > 常见的纬度包括768维，1024维，2048维。纬度越高特征越多，占用内存计算速度越慢
  ### 2.1 向量化三件套
  - (1)**模型Embedding Model**
  > 嵌入模型是一种机器学习模型，有高维度模型和低维度模型。实现在连续的低纬向量空间中表示数据的文本，图像颜色等信息，比如text-embeding-5
  - (2)**向量化数据库Embedding Store**
  > 向量存储Vector Store是一种用于存储和检索高维数据的数据库或者存储解决方案。当给定一个向量作为查询时，VectorStore返回与查询向量相似的向量。比如Qdrant
  - (3)**Embedding Search Request相似度查询***
---
  ### 2.2 第一件：Embedding Model的核心API:embed_documents 与 embed_query
  > LangChain 所有 Embedding 类都实现了两个核心方法，分别对应离线和在线场景：
  ```py
    class BaseEmbeddings:
      def embed_documents(self, texts:List[str]):
        """将多个文档文本转为向量，离线阶段批量使用，text--> List[List[float]]"""
      def embed_query(self, text:str):
        """将单个查询文本转为向量，在线阶段使用，text--> List[float]"""
  ```
  ```py
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",dimensions=512)
    
    #可选降维，省存储、提速度
    #离线:批量嵌入文档
    doc_vectors = embeddings.embed_documents([
      "员工每年享有5天带薪年假"，
      "加班需提前申请，经主管审批后方可执行"
    ])
    print(f"编码了{len(doc_vectors)}个文档，每个向量维度:{len(doc_vectors[o])}")
    #输出:编码了2个文档，每个向量维度:512
    #在线:嵌入用户查询
    query_vector=embeddings.embed_query("年假有多少天?")
    print(f"查询向量维度:{len(query_vector)}")
    #输出:查询向量维度:512
  ```
---
  ### 2.2 嵌入的步骤
    - 搜索(查询出与某字符串相关的所有结果并排名)
    - 聚类(文本字符串按照分相似性进行分组)
    - 推荐(推荐具有相关文本字符串的项目)
    - 异常检测(识别出相似性很小的异常值)
    - 多样性测量(分析相似性分布)
    - 分类(文本字符串按照最相似的标签进行分类)
---
  ### 2.3 向量计算方法
    - 欧式距离计算法
    - 余弦距离计算法
  ### 2.4 步骤：
  - 第一步：Indexing:load file--> split --> embed --> store
  - 第二步：Retrieval & Generation: question --> retrieve --> prompt --> LLM --> answer
  ### 2.5 第二件：向量数据库VectorStore
  > 📚暴力检索=在图书馆里一本一本翻找，直到找到你要的书
  > VectorStore= 图书馆的分类索引系统:先锁定哪个书架哪一排哪一本
  > 常见的向量数据库FAISS,Chroma,Milvus,Pinecone
  > langchain VectorStore的内置轻量方案包括：FAISS,Annoy,InMemoryVectorStore,适合开发测试，小规模原型验证
  > langchain VectorStore的外置专业向量数据库包括:Chroma,Pinecone(云),Milvus(分布式),Qdrant,Weaviate(云、本地),适合生产环境，大规模，持久性需求
  #### (1)VectorStore统一接口
    ```py
      class VectorStore:
        #写操作
        def add_documents(self, documents: List[Document]) -> List[str]:
        """把 Document列表嵌入并存入向量库，返回ID列表"""
        def add texts(self, texts: List[str], metadatas: List[dict] = None) -> List[str]:
        """把纯文本列表嵌入并存入向量库"""
        #检索操作
        def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """相似度检索，返回最相似的k个Document"""
        def similarity_search_with_score(self, query: str, k: int = 4) -> List[Tuple[Document, float]]
        """检索并返回相似度分数(分数越低越相似)"""
        def max_marginal_relevance_search(self, query: str, k: int = 4, fetch k: int = 20) -> List[Document]
        """MMR 检索:在相似度和多样性之间平衡，避免重复内容"""
        def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        """将 VectorStore 包装为 Retriever 对象，用于融入LCEL 链"""
    ```
  #### (2)add_documents VS add_texts
  > add_texts需要传入metadatas列表，且metadatas列表的长度必须一致且对应
    ```py
      from langchain_core.documents import Document
      docs = [
        Document(page__content=”员工每年享有5天带薪年假，由部门主管审批后即可休假。
        metadata={"source":"员工手册.pdf","page":15}),
        Document(page_content="加班需提前在 OA 系统提交申请，经主管审批后方可执行。"
        metadata={"source":"员工手册.pdf","page":28})
      ]
      ids = vectorstore.add_documents(docs)print(ids) # ['doc_0', 'doc_1']

      ids = vectorstore.add_texts(
        texts=["工作满 10年的员工，年假天数增加至10天。","公司每年组织一次全员健康体检，时间为每年6月。"],
        metadatas=[{"source":"员工手册.pdf","page":15},{"source":"员工手册.pdf","page":42}]
      )
      print(ids)  #['doc_2','doc_3']
    ```
  #### (1)Qdrant向量数据库安装
  - docker pull qdrant/qdrant
  - docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant,6333用于http浏览器界面，6334用于gRPC API
  - http://localhost:6333
  - http://localhost:6333/dashboard#/collections
  #### (2)阿里云百炼向量模型选择，比如text-embedding-v3
  #### (3)chroma向量数据库的使用
  ```py
    # pip install chromadb langchain-chroma
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursivecharacterTextsplitter
    #=====Step1:准备数据(复用前面的知识)=====
    loader = TextLoader("./员工手册.txt",encoding="utf-8")
    docs = loader.load()
    splitter = RecursivecharacterTextsplitter (chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)print(f"切成了 {len(chunks)} 个小块")
    # ===== Step 2: 初始 Embedding 和 Chroma =embeddings = OpenAIEmbeddings (model="text-embedding-3-small")
    #模式A:内存模式(临时测试，程序结束数据消失)
    vectorstore = Chroma(
      collection_name="company_policies",
      embedding_function=embeddings,
      #集合名，类似表名
      #指定Embedding模型
      #不传 persist_directory > 内存模式
    )

      #模式B:持久化模式(数据存磁盘，程序重启后依然存在)
    vectorstore = Chroma(
      collection_name="company_policies",
      embedding_function=embeddings,
      persist_directory="./chroma_db",
    )
    #指定持久化目录
    #===== Step 3:存入文档 =====
    ids = vectorstore.add_documents(chunks)
    print(f"存入了{len(ids)}条向量")
    #===== Step 4:检索 =====
    results = vectorstore.similarity_search("年假有多少天?",k=3)results_with_score = vectorstore.similarity_search_with_score("年假有多少天? ", k=3)mmr_results = vectorstore.max_marginal_relevance_search("公司]政策", k=3, fetch_k=15)
    #Chroma默认分数是L2距离，越低越相似for doc, score in results_with_score:
    print(f"L2距离: {score:.4f} | {doc.page_content[:60]}...")
  ```
---
## 三、RAG项目搭建
  ### 3.1 步骤
  - 创建项目及虚拟环境
  - 创建requirements.txt
  ```js
    flash>=3.0 // web框架，路由+静态文件托管+SSE
    openai>=1.50 // 第哦啊用deepseek 等API
    scikit-learn>=1.3 // TF-IDF文本向量化，零模型下载，纯CPU
    python-dotenv>=1.0 // 从。env文件读取API key等配置
  ```
  ### SSE解析流程
  HTTP ResponseBody(字节流) →reader.read()→TextDecoder.decode({stream:true})→拼接到buffer,按\n分割
  ### 3.3 文档分块与入库
  ### 3.4 TF-IDF向量化与检索
  ### 3.5 对话接入rag
---
## lainChain中的问答链
  - stuff：
  - map_reduce
  > 将每个document
## LLM和RAG的区别 
|      维度  |           LLM           |                       RAG                        |
|:---------:|:-----------------------:|:-------------------------------------------------:|
| 效率与成本  | 处理上下文时计算资源消耗大   |               RAG通过检索片段减少输入长度            |
| 知识更新    | 依赖上下文数据，无法更新数据 |                  连接知识库，增强时效性              |
|  可解释性   |       生成过程比较难追溯   |                检索来源透明，用户可查看来源           |
|    定制化  |        无法满足特定需求    |                可以对特定领域进行定制化检索系统        |
|  数据隐私  |           从云端检索      |   允许在本地私有化数据源上检索，避免了敏感数据上传到云端  |

## LlamaIndex和LangChain的区别
## 一、基础
## 二、进阶
## 三、实战：提示词案例
  ### 3.1 向量数据库实战chroma
  ### 3.2 搭建完整RAG应用
  ### 3.3 RAG调优
  ### 3.4 尝试dify
## 四、工程化：关键的采样参数与提示次迭代优化方法
## 五、前沿
## MCP(模型上下文协议 Model context protocol)
[!参考文章]https://blog.51cto.com/u_16213704/14714679