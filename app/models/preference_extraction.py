from pydantic import BaseModel


class PreferenceExtraction(BaseModel):
    bean_type: str | None = None
    brew_method: str | None = None
    strength: str | None = None