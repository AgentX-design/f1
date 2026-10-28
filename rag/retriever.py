from rag.vector_store import VectorStore

class Retriever:
    def __init__(self):
        self.store = VectorStore()

    def retrieve(self, query: str, top_k=3):
        return self.store.search(query, top_k)
