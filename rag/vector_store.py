import os, json, numpy as np
from rag.embeddings import EmbeddingModel

class VectorStore:
    def __init__(self, path="chroma_db/"):
        self.path = path
        self.index_path = os.path.join(path, "index.json")
        os.makedirs(path, exist_ok=True)
        self.index = []
        if os.path.exists(self.index_path):
            with open(self.index_path, encoding="utf-8") as f:
                for line in f:
                    self.index.append(json.loads(line))

    def add(self, chunks):
        for c in chunks:
            if "embedding" not in c:
                continue
            c["embedding"] = np.array(c["embedding"])
            self.index.append(c)
        self.save()

    def save(self):
        with open(self.index_path, "w", encoding="utf-8") as f:
            for item in self.index:
                item_copy = dict(item)
                item_copy["embedding"] = item_copy["embedding"].tolist()
                f.write(json.dumps(item_copy) + "\n")

    def search(self, query_text: str, top_k=3):
        model = EmbeddingModel()
        emb = model.encode([query_text])
        results = []
        for item in self.index:
            emb_item = np.array(item.get("embedding", [0]*384))
            sim = float(np.dot(emb[0], emb_item) / (np.linalg.norm(emb[0]) * np.linalg.norm(emb_item) + 1e-6))
            results.append((sim, item))
        results.sort(key=lambda x: -x[0])
        return [r[1] for r in results[:top_k]]
