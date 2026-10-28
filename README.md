# F1 History AI Chatbot
Flask chatbot for Formula 1 2021-2025 using structured fixtures, PDF ingestion pipeline, embeddings, and retrieval.

## Run
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
python app.py

## Endpoints
- GET /health
- GET /api/suggested
- POST /api/chat
- GET /api/seasons
- GET /api/sources
