import os
import fitz  # PyMuPDF

def extract_pdf(path: str, out_dir: str = "data/processed/"):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    doc = fitz.open(path)
    results = []
    for i, page in enumerate(doc):
        text = page.get_text()
        results.append({"page": i + 1, "text": text, "source": path})
    return results
