from app.config import REDIS_EXPIRY
from app.services.redis_service import RedisService


class WorkflowService:

    def __init__(self):
        self.redis = RedisService()

    def _key(self, session_id: str):
        return f"workflow:{session_id}"
    
    def start(self, session_id: str, workflow: str):
        self.redis.set(self._key(session_id), workflow, expiry=REDIS_EXPIRY)

    def get(self, session_id: str):
        return self.redis.get(self._key(session_id))
    
    def clear(self, session_id: str):
        self.redis.delete(self._key(session_id))