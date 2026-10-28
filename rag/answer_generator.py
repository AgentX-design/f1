from src.chatbot import Chatbot
from rag.retriever import Retriever
from rag.citations import format_citations

def generate_answer(question: str):
    bot = Chatbot()
    structured = bot.ask(question)
    # Avoid loading embeddings/LLM for direct structured answers
    if structured.get("retrieval") == "structured":
        return {
            "answer": structured.get("answer", "No structured answer available."),
            "sources": structured.get("sources", []),
            "retrieval_results": structured.get("retrieval_results", []),
            "retrieval_status": "structured"
        }
    # Only load vector retrieval for unclear / narrative questions
    retriever = Retriever()
    retrieved = retriever.retrieve(question, top_k=3)
    citations = format_citations(retrieved)
    return {
        "answer": structured.get("answer", "No data available."),
        "sources": structured.get("sources", []),
        "retrieval_results": citations,
        "retrieval_status": "retrieved" if retrieved else "none"
    }
