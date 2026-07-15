from rag.retriever import Retriever

retriever = Retriever()

queries = [
    "Ускорение",
    "Haste",
    "Ускорение Haste",
    "https://next.dnd.su/spells/10255-haste"
]

for query in queries:
    print("=" * 60)
    print("QUERY:", query)

    result = retriever.search(query, top_k=3)

    for meta, distance in zip(
        result["metadatas"][0],
        result["distances"][0],
    ):
        print(meta["name"], "->", distance)