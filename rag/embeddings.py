from typing import List
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    HAS_ST = True
except Exception:
    HAS_ST = False

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        if HAS_ST:
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None

    def encode(self, texts):
        if HAS_ST:
            return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Light numpy-based fallback embedding (deterministic hash-based)
        embeddings = []
        for t in texts:
            arr = np.random.RandomState(hash(str(t)) % 2**32).rand(384).astype(np.float32)
            norm = np.linalg.norm(arr) + 1e-6
            arr = arr / norm
            embeddings.append(arr)
        return np.array(embeddings)