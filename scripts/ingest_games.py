from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gamemind.data.loader import read_games_jsonl
from gamemind.rag.vector_store import GameVectorStore
from gamemind.services.embeddings import LocalHashEmbeddingProvider


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest game metadata into ChromaDB.")
    parser.add_argument("--dataset", type=Path, default=Path("data/sample_games.jsonl"))
    parser.add_argument("--chroma-path", type=Path, default=Path(".chroma"))
    parser.add_argument("--collection", default="games")
    args = parser.parse_args()

    games = read_games_jsonl(args.dataset)
    store = GameVectorStore(args.chroma_path, args.collection, LocalHashEmbeddingProvider())
    store.ingest(games)
    print(f"Indexed {store.count()} games in collection '{args.collection}'")


if __name__ == "__main__":
    main()
