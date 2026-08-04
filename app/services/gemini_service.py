from google import genai
from google.genai import types
import json
from app.config import GEMINI_MODEL
from app.models.chat_message import ChatMessage
from google.genai.errors import ClientError, ServerError
from app.exceptions.llm_exception import LLMException


class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
    
    def _generate(self, **kwargs):
        try:
            return self.client.models.generate_content(**kwargs)

        except ClientError as e:
            raise LLMException(f"Gemini client error: {e}") from e

        except ServerError as e:
            raise LLMException(f"Gemini server error: {e}") from e

        except Exception as e:
            raise LLMException(f"Unexpected Gemini error: {e}") from e

    def generate_text(self, prompt: str) -> str:
        response = self._generate(
            model=GEMINI_MODEL, contents=prompt)
        return response.text
        
    def generate_chat(self, messages: list, tools: list) -> str:
        contents = [{
            "role": message.role,
            "parts": [{"text": message.content}]} for message in messages]
        response = self._generate(
            model=GEMINI_MODEL, contents=contents,
            config=types.GenerateContentConfig(
            tools=tools),)
        return response.text
    
    def generate_json(self, prompt: str) -> dict:
        response = self._generate(
            model=GEMINI_MODEL, contents=prompt)
        return json.loads(response.text)
        

