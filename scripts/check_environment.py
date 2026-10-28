import sys
print("Python:", sys.version)
try:
    import flask, requests, pymupdf, sentence_transformers, chromadb
    print("Dependencies OK")
except Exception as e:
    print("Dependency error:", e)
