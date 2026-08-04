from app.services.gemini_service import GeminiService
from app.tools.product_tool import get_products

class CoffeeAgent:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    def chat(self, messages: list) -> str:
        return self.gemini_service.generate_chat(messages, tools=[])
