from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from gamemind.core.config import get_settings
from gamemind.data.loader import write_games_jsonl
from gamemind.data.synthetic import generate_games
from gamemind.dependencies import get_recommendation_service, get_repository, get_vector_store
from gamemind.main import app


@pytest.fixture
def test_dataset(tmp_path: Path) -> Path:
    path = tmp_path / "games.jsonl"
    write_games_jsonl(path, generate_games(60))
    return path


@pytest.fixture
def client(tmp_path: Path, test_dataset: Path) -> Iterator[TestClient]:
    get_settings.cache_clear()
    get_repository.cache_clear()
    get_vector_store.cache_clear()
    get_recommendation_service.cache_clear()

    settings = get_settings()
    settings.dataset_path = test_dataset
    settings.chroma_path = tmp_path / "chroma"
    settings.use_local_embeddings = True
    settings.use_local_ranker = True

    with TestClient(app) as test_client:
        yield test_client

    get_repository.cache_clear()
    get_vector_store.cache_clear()
    get_recommendation_service.cache_clear()
    get_settings.cache_clear()
