 from langchain_community.document_loaders import JSONLoader
    loader = JSONLoader(
        file_path = './data.json',
        jq_schema = ".[].name.age",
        text_content=False
    )
    document = loader.load()
    print(document)