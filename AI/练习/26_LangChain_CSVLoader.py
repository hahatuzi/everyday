loader = CSVLoader()
    documents = loader.load()
    for document in loader.lazy_load():
      print(document)