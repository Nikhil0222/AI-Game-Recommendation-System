from __future__ import annotations

import json
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from gamemind.services.recommendation import RecommendationService


class QueryInput(BaseModel):
    query: str = Field(description="Natural language game preference query.")


class SearchInput(BaseModel):
    query: str
    top_k: int = 10


class GenreInput(BaseModel):
    genre: str
    limit: int = 20


class RankingInput(BaseModel):
    query: str
    candidate_ids: list[str]
    top_k: int = 5


class GameMindTools:
    def __init__(self, service: RecommendationService) -> None:
        self.service = service

    def preference_extraction(self, query: str) -> dict[str, Any]:
        return self.service.preference_extractor.extract(query).model_dump()

    def genre_filtering(self, genre: str, limit: int = 20) -> list[dict[str, Any]]:
        return [
            game.model_dump()
            for game in self.service.repository.list_games(genre=genre, limit=limit)
        ]

    def similarity_search(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        self.service.ensure_indexed()
        games = {game.id: game for game in self.service.repository.all()}
        return [
            {"game": result.game.model_dump(), "score": result.score}
            for result in self.service.vector_store.search(query, games, top_k=top_k)
        ]

    def recommendation_ranking(
        self,
        query: str,
        candidate_ids: list[str],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        candidates_by_id = {
            result.game.id: result
            for result in self.service.vector_store.search(
                query,
                {game.id: game for game in self.service.repository.all()},
                top_k=max(len(candidate_ids), top_k),
            )
        }
        candidates = [
            candidates_by_id[game_id]
            for game_id in candidate_ids
            if game_id in candidates_by_id
        ]
        preferences = self.service.preference_extractor.extract(query)
        return [
            item.model_dump()
            for item in self.service.ranker.rank(query, preferences, candidates, top_k=top_k)
        ]

    def as_langchain_tools(self) -> list[StructuredTool]:
        return [
            StructuredTool.from_function(
                name="preference_extraction_tool",
                description=(
                    "Extract genres, tags, mood, time budget, and similarity hints from a query."
                ),
                func=self.preference_extraction,
                args_schema=QueryInput,
            ),
            StructuredTool.from_function(
                name="genre_filtering_tool",
                description="Filter known games by genre.",
                func=self.genre_filtering,
                args_schema=GenreInput,
            ),
            StructuredTool.from_function(
                name="similarity_search_tool",
                description="Run ChromaDB similarity search over embedded game metadata.",
                func=self.similarity_search,
                args_schema=SearchInput,
            ),
            StructuredTool.from_function(
                name="recommendation_ranking_tool",
                description="Rank retrieved candidates and return grounded recommendation reasons.",
                func=self.recommendation_ranking,
                args_schema=RankingInput,
            ),
        ]

    def tool_manifest_json(self) -> str:
        return json.dumps([tool.name for tool in self.as_langchain_tools()])
