from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
WOOCOMMERCE_URL = os.getenv("WOOCOMMERCE_URL")
WOOCOMMERCE_CONSUMER_KEY = os.getenv("WOOCOMMERCE_CONSUMER_KEY")
WOOCOMMERCE_CONSUMER_SECRET = os.getenv("WOOCOMMERCE_CONSUMER_SECRET")
WEBSITE_URL = os.getenv("WEBSITE_URL")
# Redis
REDIS_URL = os.getenv("REDIS_URL")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Redis
REDIS_EXPIRY = 60 * 60 * 24

# ChromaDB
VECTOR_DB_PATH = "./vector_db"
CHROMA_COLLECTION_NAME = "swasthya_coffee"

# Knowledge Search
KNOWLEDGE_SEARCH_RESULTS = 3

# Workflow
RECOMMENDATION_WORKFLOW = "recommendation"

# Logging
LOG_LEVEL = "INFO"