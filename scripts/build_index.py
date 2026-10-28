import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.vector_store import VectorStore
from ingestion.embed_documents import embed_chunks
store = VectorStore()
embed_chunks()
store.add([])
print("Vector index built at chroma_db/")
