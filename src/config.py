
class Config:
    """
    Configuration class to manage file paths and settings for the application.
    """

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    KNOWLEDGE_BASE_DIR = "knowledge-base"
    PERSIST_DIRECTORY = "chroma_db"
    LLM_MODEL_ID = "llama-3.3-70b-versatile"

config = Config()
