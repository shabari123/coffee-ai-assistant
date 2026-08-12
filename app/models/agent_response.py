from pydantic import BaseModel, Field
from app.models.product import Product


class AgentResponse(BaseModel):
    response: str
    products: list[Product] = Field(default_factory=list)