from services.rag_service import RAGService

class RuleService:

    def __init__(self):
        self.rag = RAGService()

    def ask(self, question: str):

        return self.rag.ask(question)