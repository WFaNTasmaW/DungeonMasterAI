from sentence_transformers import SentenceTransformer

from core.config import EMBEDDING_MODEL


class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def encode(self, text: str) -> list[float]:
        """
        Преобразует текст в эмбеддинг.
        """
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Преобразует список текстов в эмбеддинги.
        """
        return self.model.encode(texts).tolist()