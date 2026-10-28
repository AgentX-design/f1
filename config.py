import os
from dotenv import load_dotenv
load_dotenv()

DATA_DIR = os.getenv('DATA_DIR', 'data/')
VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'chroma_db/')
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'none')
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
LLM_MODEL = os.getenv('LLM_MODEL', 'openrouter/free')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-in-prod')
