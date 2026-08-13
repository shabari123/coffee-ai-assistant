import redis

from app.config import (
    REDIS_URL,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
)


class RedisService:

    def __init__(self):

        if REDIS_URL:
            self.client = redis.from_url(
                REDIS_URL,
                decode_responses=True
            )
        else:
            self.client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True
            )

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: str, expiry: int | None = None):
        if expiry:
            self.client.setex(key, expiry, value)
        else:
            self.client.set(key, value)

    def delete(self, key: str):
        self.client.delete(key)

    def exists(self, key: str):
        return self.client.exists(key)