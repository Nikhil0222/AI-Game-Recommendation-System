from pydantic import BaseModel, Field


class Game(BaseModel):
    id: str
    title: str
    genre: str
    tags: list[str] = Field(default_factory=list)
    release_year: int
    rating: float
    description: str

    def searchable_text(self) -> str:
        return (
            f"{self.title}. Genre: {self.genre}. Tags: {', '.join(self.tags)}. "
            f"Released: {self.release_year}. Rating: {self.rating}. {self.description}"
        )


class Preferences(BaseModel):
    raw_query: str
    genres: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    mood: str | None = None
    time_budget_minutes: int | None = None
    similar_to: str | None = None


class SearchResult(BaseModel):
    game: Game
    score: float


class RankedRecommendation(BaseModel):
    game: Game
    score: float
    reason: str
