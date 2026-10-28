import json, os
from rag.embeddings import EmbeddingModel

def embed_chunks(path="data/processed/chunks.jsonl"):
    model = EmbeddingModel()
    chunks = []
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    texts = [c["text"] for c in chunks]
    if not texts:
        return []
    embeddings = model.encode(texts)
    for c, emb in zip(chunks, embeddings):
        c["embedding"] = emb.tolist()
    with open("data/processed/chunks_with_embeddings.jsonl", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")
    return chunks
