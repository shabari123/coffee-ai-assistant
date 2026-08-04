import json

from app.config import REDIS_EXPIRY
from app.models.user_preference import UserPreference
from app.services.redis_service import RedisService
from app.models.preference_extraction import PreferenceExtraction

class PreferenceService:

    def __init__(self):
        self.redis = RedisService()

    def _key(self, session_id: str):
        return f"preference:{session_id}"
    
    def get(self, session_id: str) -> UserPreference:
        data = self.redis.get(
            self._key(session_id)
        )

        if not data:
            return UserPreference()

        return UserPreference(
            **json.loads(data)
        )
    
    def save(self, session_id: str, preference: UserPreference):
        self.redis.set(
            self._key(session_id),
            json.dumps(preference.model_dump()), expiry=REDIS_EXPIRY)
        
    def update(self, session_id: str, **kwargs):
        preference = self.get(session_id)

        for key, value in kwargs.items():
            setattr(preference, key, value)

        self.save(session_id, preference)

    def update_from_extraction(self, session_id: str, extraction: PreferenceExtraction):
        preference = self.get(session_id)

        if extraction.bean_type is not None:
            preference.bean_type = extraction.bean_type

        if extraction.brew_method is not None:
            preference.brew_method = extraction.brew_method

        if extraction.strength is not None:
            preference.strength = extraction.strength

        self.save(session_id, preference)