
from app.models.preference_extraction import PreferenceExtraction
from app.services.gemini_service import GeminiService


class PreferenceExtractor:

    def __init__(self, gemini_service):
        self.gemini_service = gemini_service

    def extract(self, message: str) -> PreferenceExtraction:
        prompt = f"""
                    Extract coffee preferences from the message.

                    Return ONLY valid JSON.

                    Schema:

                    {{
                        "bean_type": null,
                        "brew_method": null,
                        "strength": null
                    }}

                    Message:

                    {message}
                    """
        data = self.gemini_service.generate_json(prompt)
        return PreferenceExtraction(**data)