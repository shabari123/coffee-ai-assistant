from fastapi import APIRouter
from app.agents.router_agent import RouterAgent
from app.models.chat import ChatRequest
from app.services.chat_service import ChatService
from app.services.gemini_service import GeminiService
from app.services.conversation_service import ConversationService
from app.config import GEMINI_API_KEY
from app.agents.coffee_agent import CoffeeAgent
from app.services.preference_service import PreferenceService
from app.services.preference_extractor import PreferenceExtractor

router = APIRouter()

gemini_service = GeminiService(GEMINI_API_KEY)
coffee_agent = CoffeeAgent(gemini_service=gemini_service)
router_agent = RouterAgent(gemini_service)
conversation_service = ConversationService()
preference_service = PreferenceService()
preference_extractor = PreferenceExtractor(gemini_service)

chat_service = ChatService(
    router_agent=router_agent,
    conversation_service=conversation_service,
    preference_service=preference_service,
    preference_extractor=preference_extractor,
)

@router.post("/chat")
def chat(chat_request: ChatRequest):
    response = chat_service.chat(
        session_id=chat_request.session_id,
        message=chat_request.message,
    )

    return {
        "response": response,
    }
