from pydantic import BaseModel


class Document(BaseModel):
    title: str
    url: str
    content: str