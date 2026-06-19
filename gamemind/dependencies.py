from functools import lru_cache

from gamemind.core.config import Settings, get_settings
from gamemind.rag.vector_store import GameVectorStore
from gamemind.services.embeddings import build_embedding_provider
from gamemind.services.game_repository import GameRepository
from gamemind.services.preferences import PreferenceExtractor
from gamemind.services.ranker import build_ranker
from gamemind.services.recommendation import RecommendationService


@lru_cache
def get_repository() -> GameRepository:
    settings = get_settings()
    return GameRepository(settings.dataset_path)


@lru_cache
def get_vector_store() -> GameVectorStore:
    settings = get_settings()
    return GameVectorStore(
        settings.chroma_path,
        settings.chroma_collection,
        build_embedding_provider(settings),
    )


@lru_cache
def get_recommendation_service() -> RecommendationService:
    settings: Settings = get_settings()
    return RecommendationService(
        repository=get_repository(),
        vector_store=get_vector_store(),
        preference_extractor=PreferenceExtractor(),
        ranker=build_ranker(settings),
    )
