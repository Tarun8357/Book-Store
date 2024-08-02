from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Recommendation
from app.schemas import RecommendationSchema

class RecommendationsService:
    def __init__(self, db: Session):
        self.db = db

    def create_recommendation(self, recommendation: RecommendationSchema) -> Recommendation:
        """Create a new book recommendation."""
        db_recommendation = Recommendation(
            title=recommendation.title,
            author=recommendation.author,
            genre=recommendation.genre,
            description=recommendation.description,
            cover_image=recommendation.cover_image,
            rating=recommendation.rating,
            user_id=recommendation.user_id
        )
        self.db.add(db_recommendation)
        self.db.commit()
        self.db.refresh(db_recommendation)
        return db_recommendation

    def get_recommendations(self, skip: int = 0, limit: int = 10) -> List[RecommendationSchema]:
        """Retrieve a list of book recommendations."""
        recommendations = self.db.query(Recommendation).offset(skip).limit(limit).all()
        return [RecommendationSchema.from_orm(rec) for rec in recommendations]

    def get_recommendation_by_id(self, recommendation_id: int) -> Optional[RecommendationSchema]:
        """Retrieve a book recommendation by ID."""
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation:
            return RecommendationSchema.from_orm(recommendation)
        return None

    def update_recommendation(self, recommendation_id: int, update_data: RecommendationSchema) -> Optional[RecommendationSchema]:
        """Update an existing book recommendation."""
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(recommendation, key, value)
            self.db.commit()
            self.db.refresh(recommendation)
            return RecommendationSchema.from_orm(recommendation)
        return None

    def delete_recommendation(self, recommendation_id: int) -> bool:
        """Delete a book recommendation by ID."""
        recommendation = self.db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if recommendation:
            self.db.delete(recommendation)
            self.db.commit()
            return True
        return False
