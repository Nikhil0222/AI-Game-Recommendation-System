from __future__ import annotations

import json
from pathlib import Path

from gamemind.data.synthetic import generate_games
from gamemind.domain.models import Game


def write_games_jsonl(path: Path, games: list[Game]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for game in games:
            handle.write(game.model_dump_json() + "\n")


def read_games_jsonl(path: Path) -> list[Game]:
    if not path.exists():
        write_games_jsonl(path, generate_games())

    games: list[Game] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                games.append(Game.model_validate(json.loads(line)))
    return games
