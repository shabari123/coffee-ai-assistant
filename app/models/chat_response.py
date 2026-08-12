from pydantic import BaseModel, Field
from app.models.product import Product


class ChatResponse(BaseModel):
    response: str
    products: list[Product] = Field(default_factory=list)