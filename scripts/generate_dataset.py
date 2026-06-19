from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gamemind.data.loader import write_games_jsonl
from gamemind.data.synthetic import generate_games


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the GameMind sample game dataset.")
    parser.add_argument("--output", type=Path, default=Path("data/sample_games.jsonl"))
    parser.add_argument("--count", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    write_games_jsonl(args.output, generate_games(args.count, args.seed))
    print(f"Wrote {args.count} games to {args.output}")


if __name__ == "__main__":
    main()
