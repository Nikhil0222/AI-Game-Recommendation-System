from gamemind.services.embeddings import LocalHashEmbeddingProvider


def test_local_embeddings_are_normalized_and_deterministic() -> None:
    provider = LocalHashEmbeddingProvider(dimensions=32)
    first = provider.embed_query("relaxing crafting RPG")
    second = provider.embed_query("relaxing crafting RPG")
    assert first == second
    assert len(first) == 32
    assert abs(sum(value * value for value in first) - 1.0) < 0.0001
