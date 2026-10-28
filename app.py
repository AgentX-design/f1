import os
from flask import Flask, request, jsonify, render_template
from src.chatbot import Chatbot
from src.data_service import F1DataService
from services.chat_service import ChatService
from services.source_service import list_sources

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    data = F1DataService()
    return jsonify({
        "status":"ok",
        "structured_data_available": data.available(),
        "seasons": data.seasons(),
        "pdf_ingestion_status":"manual or automated ingestion available",
        "vector_index_available": os.path.exists("chroma_db/index.json"),
        "llm_provider_available": True if os.getenv("LLM_API_KEY") else False
    })

@app.route('/api/suggested')
def suggested():
    return jsonify([
        "Who won the 2021 Drivers' Championship?",
        "Who won the 2022 Constructors' Championship?",
        "Show 2024 Drivers' Championship standings.",
        "Give 2023 race winners.",
        "Which 2024 weekends had sprint races?"
    ])

@app.route('/api/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get('message', '')
    if not message:
        return jsonify({"error":"message required"}), 400
    service = ChatService()
    result = service.respond(message)
    return jsonify({"message": message, "result": result})

@app.route('/api/seasons')
def seasons():
    data = F1DataService()
    return jsonify({
        "seasons": data.seasons(),
        "coverage_notes":"Race results available for 2021-2025 from structured fixtures; full PDF pipeline requires raw PDFs."
    })

@app.route('/api/sources')
def sources():
    return jsonify({"sources": list_sources()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
