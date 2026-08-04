from pydantic import BaseModel


class UserPreference(BaseModel):
    bean_type: str | None = None
    brew_method: str | None = None
    strength: str | None = None
    budget: float | None = None
    roast_level: str | None = None