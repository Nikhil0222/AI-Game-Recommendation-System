from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gamemind.dependencies import get_recommendation_service

EVAL_CASES = [
    {
        "query": "I want a relaxing RPG with exploration and crafting.",
        "expected": ["RPG", "relaxing", "crafting", "exploration"],
    },
    {
        "query": "Recommend games similar to Witcher 3 but less combat focused.",
        "expected": ["story-rich", "exploration", "low combat"],
    },
    {
        "query": "I only have 30 minutes a day to play. Suggest something casual.",
        "expected": ["30-minute", "casual", "short sessions"],
    },
]


def score_case(query: str, expected: list[str]) -> dict[str, object]:
    service = get_recommendation_service()
    recommendations = service.recommend(query, top_k=5)
    expected_lc = {item.lower() for item in expected}
    relevance_hits = 0
    grounding_hits = 0
    coherence_hits = 0

    for rec in recommendations:
        metadata = " ".join([rec.game.genre, " ".join(rec.game.tags), rec.game.description]).lower()
        reason = rec.reason.lower()
        if expected_lc.intersection(metadata.split()) or any(
            term in metadata for term in expected_lc
        ):
            relevance_hits += 1
        if rec.game.title.lower() in reason or any(tag.lower() in reason for tag in rec.game.tags):
            grounding_hits += 1
        if len(rec.reason.split()) >= 8 and rec.reason.endswith("."):
            coherence_hits += 1

    total = max(len(recommendations), 1)
    return {
        "query": query,
        "relevance": relevance_hits / total,
        "grounding": grounding_hits / total,
        "coherence": coherence_hits / total,
        "recommendations": [rec.game.title for rec in recommendations],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GameMind recommendation evaluation.")
    parser.add_argument("--output", type=Path, default=Path("evaluation_report.json"))
    args = parser.parse_args()

    cases = [score_case(case["query"], case["expected"]) for case in EVAL_CASES]
    summary = {
        metric: sum(float(case[metric]) for case in cases) / len(cases)
        for metric in ["relevance", "grounding", "coherence"]
    }
    report = {"summary": summary, "cases": cases}
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
