import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek API Configuration
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    
    # Model Configuration - Optimized for cost
    MODEL_NAME = "deepseek-chat"
    MAX_TOKENS = 4096  # Increased for complete policy responses
    TEMPERATURE = 0.1
    
    # Vector Database Configuration
    CHROMA_DB_PATH = "./chroma_db"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight model
    
    # Document Processing - Enhanced organization paths
    DOCUMENTS_PATH = "./documents"
    EXTRACTED_PATH = "./kfg_policy/cleaned_documents"  # Legacy path
    ORGANIZED_PATH = "./kfg_policy/organized"  # New organized documents
    METADATA_PATH = "./kfg_policy/metadata"    # Document metadata
    ORIGINAL_PATH = "./kfg_policy"             # Original policy files
    PROCESSED_PATH = "./kfg_policy/processed"
    
    # Chunking - File-based chunking for complete policy context
    CHUNK_SIZE = 0  # No chunking - each file is one chunk
    CHUNK_OVERLAP = 0  # No overlap needed
    MAX_CHUNK_SIZE = 0  # No maximum - entire file content
    
    # Translation Configuration
    TRANSLATE_TO_BANGLA = True
    BANGLA_MODEL = "Helsinki-NLP/opus-mt-en-bn"
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.txt']
    
    # Chat Configuration - Optimized for better answers
    MAX_HISTORY = 3  # Reduced for cost control
    SIMILARITY_THRESHOLD = 0.3  # Lowered to allow more relevant documents
    
    # Cost Control Settings - Balanced for quality and cost
    MAX_DOCUMENTS_PER_QUERY = 5  # Increased for better coverage
    MAX_CONTEXT_LENGTH = 8000    # Increased for better context and complete policy coverage
    MIN_SIMILARITY_SCORE = 0.2   # Lowered minimum similarity for better coverage
    
    # Document Processing
    ENABLE_OCR = True
    ENABLE_TRANSLATION = False  # Disable for cost control
    SAVE_PROCESSING_RESULTS = True
    
    # Enhanced Search Settings
    ENABLE_CATEGORY_FILTERING = True
    ENABLE_TYPE_FILTERING = True
    MAX_SEARCH_RESULTS = 10
    
    # Confidence Analysis Settings
    HIGH_CONFIDENCE_THRESHOLD = 0.7    # Documents with 0.7+ similarity are high confidence
    MEDIUM_CONFIDENCE_THRESHOLD = 0.5  # Documents with 0.5-0.7 similarity are medium confidence
    LOW_CONFIDENCE_THRESHOLD = 0.5     # Documents below 0.5 are low confidence
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "kfg_chatbot.log" 