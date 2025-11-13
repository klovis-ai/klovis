from klovis.loaders.text_file_loader import TextFileLoader

loader = TextFileLoader(encoding="utf-8", skip_empty=True)
docs = loader.load(["data/example1.txt", "data/example2.txt"])

for doc in docs:
    print(doc.to_dict())