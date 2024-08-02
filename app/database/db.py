from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self) -> Generator[Session, None, None]:
        """Provide a database session to be used in FastAPI dependency injection."""
        db: Session = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()