from gamemind.data.loader import read_games_jsonl
from gamemind.services.game_repository import GameRepository


def test_repository_filters_by_genre_and_tag(test_dataset) -> None:
    repository = GameRepository(test_dataset)
    rpgs = repository.list_games(genre="RPG", limit=10)
    assert rpgs
    assert all(game.genre == "RPG" for game in rpgs)

    crafting = repository.list_games(tag="crafting", limit=10)
    assert crafting
    assert all("crafting" in game.tags for game in crafting)
    assert repository.get_many([rpgs[0].id, "missing"]) == [rpgs[0]]


def test_loader_generates_missing_dataset(tmp_path) -> None:
    path = tmp_path / "missing.jsonl"
    games = read_games_jsonl(path)
    assert path.exists()
    assert len(games) == 500
