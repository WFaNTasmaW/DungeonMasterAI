from rag.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from knowledge.loaders import MonsterLoader, SpellLoader, ClassLoader
from rag.indexer import Indexer


class Retriever:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.monsters = MonsterLoader().load()
        self.spells = SpellLoader().load()
        self.classes = ClassLoader().load()

    def search(
            self,
            query: str,
            top_k: int = 5,
    ):
        embedding = self.embedding_model.encode(query)

        return self.vector_store.query(
            embedding=embedding,
            n_results=top_k,
        )