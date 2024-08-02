from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.recommendations_schema import RecommendationSchema
from app.services.recommendations_service import RecommendationsService

class RecommendationsRouter:
    def __init__(self):
        self.router = APIRouter()
        self.service = RecommendationsService()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/", self.submit_recommendation, methods=["POST"], response_model=RecommendationSchema)
        self.router.add_api_route("/", self.get_recommendations, methods=["GET"], response_model=List[RecommendationSchema])
        self.router.add_api_route("/{recommendation_id}", self.get_recommendation, methods=["GET"], response_model=RecommendationSchema)
        self.router.add_api_route("/{recommendation_id}", self.update_recommendation, methods=["PUT"], response_model=RecommendationSchema)
        self.router.add_api_route("/{recommendation_id}", self.delete_recommendation, methods=["DELETE"], response_model=bool)

    async def submit_recommendation(self, recommendation: RecommendationSchema):
        return await self.service.add_recommendation(recommendation)

    async def get_recommendations(self):
        return await self.service.get_recommendations()

    async def get_recommendation(self, recommendation_id: int):
        recommendation = await self.service.get_recommendation_by_id(recommendation_id)
        if recommendation:
            return recommendation
        raise HTTPException(status_code=404, detail="Recommendation not found")

    async def update_recommendation(self, recommendation_id: int, recommendation: RecommendationSchema):
        updated_recommendation = await self.service.update_recommendation(recommendation_id, recommendation)
        if updated_recommendation:
            return updated_recommendation
        raise HTTPException(status_code=404, detail="Recommendation not found")

    async def delete_recommendation(self, recommendation_id: int):
        success = await self.service.delete_recommendation(recommendation_id)
        if success:
            return True
        raise HTTPException(status_code=404, detail="Recommendation not found")
