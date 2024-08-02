from dotenv import load_dotenv
import os

class Config:
    """Configuration class for managing environment variables and settings."""

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # API key for Google Books API
        self.GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

    def get_google_books_api_key(self):
        """Get the Google Books API key."""
        if not self.GOOGLE_BOOKS_API_KEY:
            raise ValueError("Google Books API key is not set in environment variables.")
        return self.GOOGLE_BOOKS_API_KEY

# Create a singleton instance of the configuration
config = Config()
