from typing import List, Dict

def format_citations(results: List[Dict]) -> List[Dict]:
    citations = []
    for r in results:
        citations.append({
            "chunk_id": r.get("chunk_id", "unknown"),
            "doc_id": r.get("doc_id", "unknown"),
            "season": r.get("season"),
            "text_preview": (r.get("text", "")[:200] + "...")
        })
    return citations
