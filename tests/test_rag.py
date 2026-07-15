from services.rag_service import RAGService

rag = RAGService()

question = input("Введите вопрос: ")

answer = rag.ask(question)

print(answer)