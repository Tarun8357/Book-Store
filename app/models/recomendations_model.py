from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    description = Column(Text)
    cover_image = Column(String)
    rating = Column(Float)
    user_id = Column(Integer)  # Assuming you have a user model
