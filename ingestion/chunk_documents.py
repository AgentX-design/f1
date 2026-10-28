import json, os
from ingestion.clean_text import clean_text

def chunk_text(text: str, doc_id: str, season: int = 2024):
    words = text.split()
    chunks = []
    size = 400
    overlap = 60
    for i in range(0, len(words), size - overlap):
        chunk_words = words[i:i+size]
        chunk_text = " ".join(chunk_words)
        chunks.append({
            "chunk_id": f"{doc_id}-{i}",
            "doc_id": doc_id,
            "season": season,
            "text": chunk_text,
            "index": i
        })
    return chunks

def write_chunks(chunks, out_path="data/processed/chunks.jsonl"):
    with open(out_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c) + "\n")
