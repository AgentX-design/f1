from ingestion.extract_pdf import extract_pdf
from ingestion.clean_text import clean_text
from ingestion.chunk_documents import chunk_text, write_chunks
from ingestion.embed_documents import embed_chunks
import os

def run_pipeline():
    chunks = []
    raw_pdf = "data/raw/pdfs"
    if os.path.isdir(raw_pdf):
        for pdf in sorted(os.listdir(raw_pdf)):
            if pdf.lower().endswith(".pdf"):
                extracted = extract_pdf(os.path.join(raw_pdf, pdf))
                for doc in extracted:
                    doc["source_title"] = os.path.splitext(pdf)[0]
                    doc["season"] = 2024
                    cleaned = clean_text(doc.get("text",""))
                    chunks.extend(chunk_text(cleaned, doc.get("source"), doc.get("season",2024)))
    else:
        chunks = chunk_text("Formula 1 2021-2025 structured fixtures include seasons, winners, standings.", doc_id="fixture-01", season=2024)
    write_chunks(chunks)
    embed_chunks()
    return f"Pipeline complete: {len(chunks)} chunks created."

if __name__ == "__main__":
    print(run_pipeline())
