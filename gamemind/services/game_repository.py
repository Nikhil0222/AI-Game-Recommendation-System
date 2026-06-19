from pathlib import Path

from gamemind.data.loader import read_games_jsonl
from gamemind.domain.models import Game


class GameRepository:
    def __init__(self, dataset_path: Path) -> None:
        self.dataset_path = dataset_path
        self._games = read_games_jsonl(dataset_path)
        self._by_id = {game.id: game for game in self._games}

    def list_games(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        genre: str | None = None,
        tag: str | None = None,
    ) -> list[Game]:
        games = self._games
        if genre:
            games = [game for game in games if game.genre.casefold() == genre.casefold()]
        if tag:
            games = [game for game in games if tag.casefold() in {t.casefold() for t in game.tags}]
        return games[offset : offset + limit]

    def count(self) -> int:
        return len(self._games)

    def get_many(self, ids: list[str]) -> list[Game]:
        return [self._by_id[game_id] for game_id in ids if game_id in self._by_id]

    def all(self) -> list[Game]:
        return list(self._games)
