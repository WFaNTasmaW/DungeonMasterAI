import chromadb

from core.config import CHROMA_DB_PATH


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

        self.collection = self.client.get_or_create_collection(
            name="dnd_knowledge"
        )

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ):

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(
        self,
        embedding: list[float],
        n_results: int = 5,
    ):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
        )

    def count(self):

        return self.collection.count()

    def delete_all(self):

        self.client.delete_collection("dnd_knowledge")

        self.collection = self.client.get_or_create_collection(
            name="dnd_knowledge"
        )