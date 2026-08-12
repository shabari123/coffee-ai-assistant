import json

from app.config import REDIS_EXPIRY
from app.models.chat_message import ChatMessage
from app.services.redis_service import RedisService


class ConversationService:
    def __init__(self):
        self.redis = RedisService()

    def _key(self, session_id: str) -> str:
        return f"conversation:{session_id}"

    def get_history(self, session_id: str) -> list[ChatMessage]:
        data = self.redis.get(self._key(session_id))
        if not data:
            return []

        messages = json.loads(data)
        return [
            ChatMessage(**message)
            for message in messages
        ]

    def save_history(self, session_id: str, messages: list[ChatMessage]) -> None:
        data = json.dumps(
            [
                message.model_dump()
                for message in messages
            ]
        )

        self.redis.set(
            self._key(session_id),
            data, expiry=REDIS_EXPIRY
        )

    def add_user_message(self, session_id: str, message: str) -> None:
        history = self.get_history(session_id)

        history.append(
            ChatMessage(
                role="user",
                content=message,
            )
        )

        self.save_history(session_id, history)

    def add_assistant_message(self, session_id: str, message: str) -> None:
        history = self.get_history(session_id)

        history.append(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

        self.save_history(session_id, history)

    def clear_history(self, session_id: str) -> None:

        self.redis.delete(
            self._key(session_id)
        )