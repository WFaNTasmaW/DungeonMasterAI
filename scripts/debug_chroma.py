from rag.vector_store import VectorStore

store = VectorStore()

collection = store.collection

print("Всего документов:", collection.count())

result = collection.get()

for doc, meta in zip(result["documents"], result["metadatas"]):
    if meta["type"] == "spell" and "Ускорение" in meta["name"]:
        print("=" * 60)
        print(meta)
        print(doc)