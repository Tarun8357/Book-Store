from pydantic import BaseModel, HttpUrl
from typing import Optional

class RecommendationSchema(BaseModel):
    title: str
    author: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[HttpUrl] = None
    rating: Optional[float] = None
    user_id: Optional[int] = None

    class Config:
        orm_mode = True
