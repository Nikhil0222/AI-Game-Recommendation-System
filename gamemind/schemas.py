from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    query: str = Field(min_length=3, examples=["I want a relaxing RPG with exploration."])
    top_k: int | None = Field(default=None, ge=1, le=10)


class RecommendationItem(BaseModel):
    title: str
    genre: str
    tags: list[str]
    release_year: int
    rating: float
    score: float
    reason: str


class RecommendationResponse(BaseModel):
    query: str
    recommendations: list[RecommendationItem]


class GameItem(BaseModel):
    id: str
    title: str
    genre: str
    tags: list[str]
    release_year: int
    rating: float
    description: str


class GamesResponse(BaseModel):
    count: int
    games: list[GameItem]


class HealthResponse(BaseModel):
    status: str
    version: str
    indexed_games: int
