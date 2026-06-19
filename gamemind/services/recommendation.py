from gamemind.core.errors import NotReadyError
from gamemind.domain.models import RankedRecommendation
from gamemind.rag.vector_store import GameVectorStore
from gamemind.services.game_repository import GameRepository
from gamemind.services.preferences import PreferenceExtractor
from gamemind.services.ranker import RecommendationRanker


class RecommendationService:
    def __init__(
        self,
        repository: GameRepository,
        vector_store: GameVectorStore,
        preference_extractor: PreferenceExtractor,
        ranker: RecommendationRanker,
    ) -> None:
        self.repository = repository
        self.vector_store = vector_store
        self.preference_extractor = preference_extractor
        self.ranker = ranker

    def ensure_indexed(self) -> None:
        if self.vector_store.count() == 0:
            self.vector_store.ingest(self.repository.all())

    def recommend(self, query: str, *, top_k: int = 5) -> list[RankedRecommendation]:
        if self.repository.count() == 0:
            raise NotReadyError("Game dataset is empty.")

        self.ensure_indexed()
        preferences = self.preference_extractor.extract(query)
        genre_filter = preferences.genres[0] if len(preferences.genres) == 1 else None
        retrieval_query = " ".join(
            part
            for part in [query, preferences.mood or "", " ".join(preferences.tags)]
            if part
        )
        candidates = self.vector_store.search(
            retrieval_query,
            {game.id: game for game in self.repository.all()},
            top_k=max(top_k * 4, 20),
            genre=genre_filter,
        )
        if not candidates:
            raise NotReadyError("No indexed games were available for recommendation.")
        return self.ranker.rank(query, preferences, candidates, top_k=top_k)
