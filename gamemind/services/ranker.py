from __future__ import annotations

import json
from abc import ABC, abstractmethod

from gamemind.core.config import Settings
from gamemind.domain.models import Preferences, RankedRecommendation, SearchResult


class RecommendationRanker(ABC):
    @abstractmethod
    def rank(
        self,
        query: str,
        preferences: Preferences,
        candidates: list[SearchResult],
        *,
        top_k: int,
    ) -> list[RankedRecommendation]:
        raise NotImplementedError


class LocalRecommendationRanker(RecommendationRanker):
    def rank(
        self,
        query: str,
        preferences: Preferences,
        candidates: list[SearchResult],
        *,
        top_k: int,
    ) -> list[RankedRecommendation]:
        ranked: list[RankedRecommendation] = []
        requested_tags = {tag.casefold() for tag in preferences.tags}
        requested_genres = {genre.casefold() for genre in preferences.genres}
        wants_less_combat = "low combat" in requested_tags

        for candidate in candidates:
            game = candidate.game
            game_tags = {tag.casefold() for tag in game.tags}
            tag_overlap = requested_tags.intersection(game_tags)
            genre_match = game.genre.casefold() in requested_genres if requested_genres else False
            time_match = self._time_match(preferences.time_budget_minutes, game.tags)
            score = candidate.score + (0.08 * len(tag_overlap)) + (0.12 if genre_match else 0.0)
            score += 0.08 if time_match else 0.0
            if wants_less_combat and "low combat" not in game_tags and "combat" in game_tags:
                score -= 0.15
            reason_bits = []
            if genre_match:
                reason_bits.append(f"matches the requested {game.genre} genre")
            if tag_overlap:
                reason_bits.append(f"aligns on {', '.join(sorted(tag_overlap))}")
            if time_match:
                reason_bits.append("fits short daily play sessions")
            if not reason_bits:
                reason_bits.append("is semantically close to the preference text")
            reason = f"{game.title} is recommended because it " + " and ".join(reason_bits) + "."
            ranked.append(RankedRecommendation(game=game, score=round(score, 4), reason=reason))

        ranked.sort(key=lambda item: (item.score, item.game.rating), reverse=True)
        return ranked[:top_k]

    @staticmethod
    def _time_match(minutes: int | None, tags: list[str]) -> bool:
        if minutes is None:
            return False
        tag_set = {tag.casefold() for tag in tags}
        return minutes <= 30 and ({"15-minute", "30-minute", "short sessions", "casual"} & tag_set)


class OpenAIRecommendationRanker(RecommendationRanker):  # pragma: no cover
    def __init__(self, settings: Settings) -> None:
        from langchain_openai import ChatOpenAI

        self._llm = ChatOpenAI(
            model=settings.openai_chat_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
        )
        self._fallback = LocalRecommendationRanker()

    def rank(
        self,
        query: str,
        preferences: Preferences,
        candidates: list[SearchResult],
        *,
        top_k: int,
    ) -> list[RankedRecommendation]:
        compact_candidates = [
            {
                "id": candidate.game.id,
                "title": candidate.game.title,
                "genre": candidate.game.genre,
                "tags": candidate.game.tags,
                "rating": candidate.game.rating,
                "description": candidate.game.description,
                "retrieval_score": candidate.score,
            }
            for candidate in candidates[: min(len(candidates), 20)]
        ]
        prompt = (
            "You are GameMind, a grounded video game recommendation agent. "
            "Rank only the provided candidates for the user query. Return JSON with a "
            "'recommendations' array of objects: id, score from 0 to 1, reason. "
            "Each reason must cite candidate metadata, not outside facts.\n\n"
            f"Query: {query}\n"
            f"Extracted preferences: {preferences.model_dump_json()}\n"
            f"Candidates: {json.dumps(compact_candidates)}\n"
            f"Return exactly {top_k} recommendations."
        )
        try:
            response = self._llm.invoke(prompt)
            payload = json.loads(str(response.content))
            by_id = {candidate.game.id: candidate for candidate in candidates}
            ranked = []
            for item in payload.get("recommendations", []):
                candidate = by_id.get(item.get("id"))
                if candidate:
                    ranked.append(
                        RankedRecommendation(
                            game=candidate.game,
                            score=float(item.get("score", candidate.score)),
                            reason=str(item.get("reason", "")) or "Strong metadata match.",
                        )
                    )
            return ranked[:top_k] or self._fallback.rank(
                query,
                preferences,
                candidates,
                top_k=top_k,
            )
        except Exception:
            return self._fallback.rank(query, preferences, candidates, top_k=top_k)


def build_ranker(settings: Settings) -> RecommendationRanker:
    if settings.use_local_ranker or not settings.openai_api_key:
        return LocalRecommendationRanker()
    return OpenAIRecommendationRanker(settings)
