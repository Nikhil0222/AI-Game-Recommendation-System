from __future__ import annotations

from pathlib import Path

import chromadb

from gamemind.domain.models import Game, SearchResult
from gamemind.services.embeddings import EmbeddingProvider


class GameVectorStore:
    def __init__(
        self,
        chroma_path: Path,
        collection_name: str,
        embeddings: EmbeddingProvider,
    ) -> None:
        chroma_path.mkdir(parents=True, exist_ok=True)
        self.embeddings = embeddings
        self.client = chromadb.PersistentClient(path=str(chroma_path))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "GameMind video game recommendation corpus"},
        )

    def ingest(self, games: list[Game], *, batch_size: int = 100) -> None:
        for start in range(0, len(games), batch_size):
            batch = games[start : start + batch_size]
            documents = [game.searchable_text() for game in batch]
            self.collection.upsert(
                ids=[game.id for game in batch],
                documents=documents,
                metadatas=[
                    {
                        "title": game.title,
                        "genre": game.genre,
                        "release_year": game.release_year,
                        "rating": game.rating,
                        "tags": ", ".join(game.tags),
                    }
                    for game in batch
                ],
                embeddings=self.embeddings.embed_documents(documents),
            )

    def count(self) -> int:
        return self.collection.count()

    def search(
        self,
        query: str,
        games_by_id: dict[str, Game],
        *,
        top_k: int = 20,
        genre: str | None = None,
    ) -> list[SearchResult]:
        where = {"genre": genre} if genre else None
        result = self.collection.query(
            query_embeddings=[self.embeddings.embed_query(query)],
            n_results=top_k,
            where=where,
            include=["distances"],
        )
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]
        search_results: list[SearchResult] = []
        for game_id, distance in zip(ids, distances, strict=False):
            game = games_by_id.get(game_id)
            if game:
                search_results.append(SearchResult(game=game, score=1 / (1 + float(distance))))
        return search_results
