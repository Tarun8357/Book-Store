from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookSchema

class BooksService:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookSchema) -> Book:
        """Create a new book record."""
        db_book = Book(
            title=book.title,
            author=book.author,
            genre=book.genre,
            description=book.description,
            cover_image=book.cover_image,
            rating=book.rating
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_books(self, skip: int = 0, limit: int = 10) -> List[BookSchema]:
        """Retrieve a list of book records."""
        books = self.db.query(Book).offset(skip).limit(limit).all()
        return [BookSchema.from_orm(b) for b in books]

    def get_book_by_id(self, book_id: int) -> Optional[BookSchema]:
        """Retrieve a book record by ID."""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            return BookSchema.from_orm(book)
        return None

    def update_book(self, book_id: int, update_data: BookSchema) -> Optional[BookSchema]:
        """Update an existing book record."""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(book, key, value)
            self.db.commit()
            self.db.refresh(book)
            return BookSchema.from_orm(book)
        return None

    def delete_book(self, book_id: int) -> bool:
        """Delete a book record by ID."""
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if book:
            self.db.delete(book)
            self.db.commit()
            return True
        return False
