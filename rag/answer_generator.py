from rag.retriever import Retriever
from rag.citations import format_citations
from src.chatbot import Chatbot

def generate_answer(question: str):
    bot = Chatbot()
    structured = bot.ask(question)
    retriever = Retriever()
    retrieved = retriever.retrieve(question, top_k=3)
    citations = format_citations(retrieved)
    if structured.get("retrieval") == "structured" or citations:
        return {
            "answer": structured.get("answer", "No structured answer available."),
            "sources": structured.get("sources", []),
            "retrieval_results": citations,
            "retrieval_status": "retrieved" if retrieved else "none"
        }
    return {
        "answer": structured.get("answer", "No data available."),
        "sources": structured.get("sources", []),
        "retrieval_results": citations,
        "retrieval_status": "retrieved" if retrieved else "none"
    }
