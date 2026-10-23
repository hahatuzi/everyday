loader = PyPDFLoader(
      file_path="./data/pdf1.pdf"
    )
    i = 0
    for doc in loader.lazy_load():
      i++