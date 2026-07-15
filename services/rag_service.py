from llm.client import LLMClient
from llm.prompts import RULE_ASSISTANT_PROMPT
from rag.data_filter import DataFilter
from rag.indexer import Indexer

from rag.retriever import Retriever


class RAGService:

    def __init__(self):

        self.retriever = Retriever()
        self.llm = LLMClient()
        self.filter = DataFilter()

    def ask(self, question: str, top_k: int = 5) -> str:

        objects = self.filter.filter(question)

        if objects:

            documents = []

            for obj in objects:

                if hasattr(obj, "school"):
                    documents.append(
                        Indexer.spell_to_document(obj)
                    )

                elif hasattr(obj, "challenge_rating"):
                    documents.append(
                        Indexer.monster_to_document(obj)
                    )

                else:
                    documents.append(
                        Indexer.class_to_document(obj)
                    )

            context = "\n\n".join(documents)

        else:

            search_result = self.retriever.search(
                question,
                top_k=top_k
            )

            context = "\n\n".join(
                search_result["documents"][0]
            )

        messages = [
            {
                "role": "system",
                "content": RULE_ASSISTANT_PROMPT
            },
            {
                "role": "user",
                "content": f"""
    Используй приведенный ниже контекст, чтобы ответить на вопрос.

    Контекст:

    {context}

    ----------------------

    Вопрос:

    {question}
    """
            }
        ]

        return self.llm.chat(messages)