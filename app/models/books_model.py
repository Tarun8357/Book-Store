from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String)
    description = Column(Text)
    cover_image = Column(String)
    rating = Column(Float)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
