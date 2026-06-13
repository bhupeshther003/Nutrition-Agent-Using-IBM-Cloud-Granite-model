import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', 'vector_db')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # IBM Watsonx.ai Configuration
    WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
    WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
    WATSONX_URL = os.getenv('WATSONX_URL', 'https://au-syd.ml.cloud.ibm.com')
    
    # Model Configuration
    WATSONX_MODEL_ID = os.getenv('WATSONX_MODEL_ID', 'ibm/granite-3-3-8b-instruct')
    WATSONX_MAX_TOKENS = int(os.getenv('WATSONX_MAX_TOKENS', 500))
    WATSONX_TEMPERATURE = float(os.getenv('WATSONX_TEMPERATURE', 0.7))
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 3
    
    @staticmethod
    def init_app(app):
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)

# Made with Bob
