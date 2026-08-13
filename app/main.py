from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.config import GEMINI_API_KEY
from app.services.gemini_service import GeminiService
from app.api.chat import router as chat_router
import logging
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://swasthya-coffee-ui.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Swasthya Coffee AI Assistant"
    }


app.include_router(chat_router)
