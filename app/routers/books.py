from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.book_schema import BookSchema
from app.services.books_service import BooksService
from app.services import GoogleBooksService
from app.database import get_db
from app.models import Book

class BooksRouter:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/search", self.search_books, methods=["GET"], response_model=List[BookSchema])
        self.router.add_api_route("/{book_id}", self.get_book_by_id, methods=["GET"], response_model=BookSchema)
        self.router.add_api_route("/", self.create_book, methods=["POST"], response_model=BookSchema)
        self.router.add_api_route("/", self.get_books, methods=["GET"], response_model=List[BookSchema])
        self.router.add_api_route("/{book_id}", self.get_book, methods=["GET"], response_model=BookSchema)
        self.router.add_api_route("/{book_id}", self.update_book, methods=["PUT"], response_model=BookSchema)
        self.router.add_api_route("/{book_id}", self.delete_book, methods=["DELETE"], response_model=dict)

    async def search_books(self, query: str, max_results: int = 10):
        """Search for books using the Google Books API."""
        try:
            books = google_books_service.search_books(query, max_results)
            return books
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_book_by_id(self, book_id: str):
        """Retrieve a single book's details using the Google Books API."""
        try:
            book = google_books_service.get_book_by_id(book_id)
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            return book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_book(self, book: BookSchema, db: Session = Depends(get_db), service: BooksService = Depends()):
        """Create a new book record."""
        try:
            created_book = service.create_book(book)
            return created_book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_books(self, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), service: BooksService = Depends()):
        """Retrieve a list of book records."""
        try:
            books = service.get_books(skip, limit)
            return books
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_book(self, book_id: int, db: Session = Depends(get_db), service: BooksService = Depends()):
        """Retrieve a book record by ID."""
        try:
            book = service.get_book_by_id(book_id)
            if book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            return book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_book(self, book_id: int, update_data: BookSchema, db: Session = Depends(get_db), service: BooksService = Depends()):
        """Update an existing book record."""
        try:
            updated_book = service.update_book(book_id, update_data)
            if updated_book is None:
                raise HTTPException(status_code=404, detail="Book not found")
            return updated_book
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_book(self, book_id: int, db: Session = Depends(get_db), service: BooksService = Depends()):
        """Delete a book record by ID."""
        try:
            success = service.delete_book(book_id)
            if not success:
                raise HTTPException(status_code=404, detail="Book not found")
            return {"detail": "Book deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

