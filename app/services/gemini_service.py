
from google import genai
from google.genai import types
import json
from app.config import GEMINI_MODEL
from app.models.chat_message import ChatMessage
from google.genai.errors import ClientError, ServerError
from app.exceptions.llm_exception import LLMException
from app.models.gemini_response import GeminiResponse


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
        
    def generate_chat(self, messages: list, tools: list) -> GeminiResponse:
        contents = [
            {
                "role": message.role,
                "parts": [{"text": message.content}]
            }
            for message in messages
        ]

        response = self._generate(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction="""
    You are the Swasthya Coffee AI Assistant.

    When you use a product tool, the application will render the
    product information separately as product cards.

    IMPORTANT:
    - Do NOT list product names, prices, descriptions, URLs, or stock status
    in your response when the product tool has returned products.
    - Do NOT reproduce the product list returned by a tool.
    - Keep your response short and conversational.
    - You can introduce or summarize the results.
    - For example:
    "Here are the coffee options currently available."

    If the user asks about one specific product, you may explain that product
    in natural language, but avoid duplicating the product card information.
    """,
            ),
        )

        tool_results = []

        for content in response.automatic_function_calling_history:
            for part in content.parts:
                if part.function_response:
                    tool_results.append(part.function_response.response)

        return GeminiResponse(
            text=response.text,
            tool_results=tool_results,
        )
    
    def generate_json(self, prompt: str) -> dict:
        response = self._generate(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

        return json.loads(response.text)
            

