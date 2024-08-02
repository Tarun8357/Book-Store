import requests
from typing import List, Optional
from app.schemas import BookSchema
from app.config import config

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

class GoogleBooksService:
    def __init__(self):
        self.api_key = config.get_google_books_api_key()

    def _get_request_params(self, query: str, max_results: int = 10) -> dict:
        """Construct the query parameters for the Google Books API request."""
        return {
            "q": query,
            "maxResults": max_results,
            "key": self.api_key
        }

    def search_books(self, query: str, max_results: int = 10) -> List[BookSchema]:
        """Search for books using the Google Books API."""
        params = self._get_request_params(query, max_results)
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        books = []

        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            book = BookSchema(
                title=volume_info.get("title", ""),
                author=", ".join(volume_info.get("authors", [])),
                genre=", ".join(volume_info.get("categories", [])),
                description=volume_info.get("description", ""),
                cover_image=volume_info.get("imageLinks", {}).get("thumbnail"),
                rating=volume_info.get("averageRating")
            )
            books.append(book)

        return books

    def get_book_by_id(self, book_id: str) -> Optional[BookSchema]:
        """Retrieve a single book's details using the Google Books API."""
        params = {
            "q": f"id:{book_id}",
            "key": self.api_key
        }
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        item = data.get("items", [{}])[0]
        volume_info = item.get("volumeInfo", {})

        return BookSchema(
            title=volume_info.get("title", ""),
            author=", ".join(volume_info.get("authors", [])),
            genre=", ".join(volume_info.get("categories", [])),
            description=volume_info.get("description", ""),
            cover_image=volume_info.get("imageLinks", {}).get("thumbnail"),
            rating=volume_info.get("averageRating")
        ) if volume_info else None

