from gamemind.data.loader import read_games_jsonl, write_games_jsonl
from gamemind.data.synthetic import generate_games


def test_generate_games_has_required_fields() -> None:
    games = generate_games(500)
    assert len(games) == 500
    assert games[0].title
    assert games[0].genre
    assert games[0].tags
    assert games[0].release_year >= 2005
    assert 0 <= games[0].rating <= 5
    assert games[0].description


def test_jsonl_round_trip(tmp_path) -> None:
    path = tmp_path / "games.jsonl"
    games = generate_games(3)
    write_games_jsonl(path, games)
    loaded = read_games_jsonl(path)
    assert [game.id for game in loaded] == [game.id for game in games]
