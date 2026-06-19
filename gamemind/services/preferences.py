import re

from gamemind.domain.models import Preferences

GENRE_KEYWORDS = {
    "rpg": "RPG",
    "role playing": "RPG",
    "strategy": "Strategy",
    "simulation": "Simulation",
    "sim": "Simulation",
    "puzzle": "Puzzle",
    "roguelike": "Roguelike",
    "platformer": "Platformer",
    "narrative": "Narrative",
    "survival": "Survival",
    "sports": "Sports",
    "action": "Action Adventure",
    "adventure": "Action Adventure",
}

TAG_KEYWORDS = [
    "relaxing",
    "cozy",
    "crafting",
    "exploration",
    "casual",
    "short sessions",
    "low combat",
    "story-rich",
    "open world",
    "management",
    "turn-based",
    "co-op",
]

MOODS = ["relaxing", "cozy", "challenging", "casual", "focused", "emotional", "tense", "epic"]


class PreferenceExtractor:
    def extract(self, query: str) -> Preferences:
        query_lc = query.lower()
        genres = [
            genre
            for keyword, genre in GENRE_KEYWORDS.items()
            if re.search(rf"\b{re.escape(keyword)}\b", query_lc)
        ]
        tags = [tag for tag in TAG_KEYWORDS if tag in query_lc]
        if "less combat" in query_lc or "no combat" in query_lc:
            tags.append("low combat")
        mood = next((candidate for candidate in MOODS if candidate in query_lc), None)
        time_budget = self._extract_time_budget(query_lc)
        similar_to = self._extract_similar_to(query)
        if similar_to and "witcher" in similar_to.lower():
            tags.extend(["story-rich", "exploration", "open world"])
        return Preferences(
            raw_query=query,
            genres=list(dict.fromkeys(genres)),
            tags=list(dict.fromkeys(tags)),
            mood=mood,
            time_budget_minutes=time_budget,
            similar_to=similar_to,
        )

    @staticmethod
    def _extract_time_budget(query: str) -> int | None:
        match = re.search(r"(\d+)\s*(minutes?|mins?)", query)
        return int(match.group(1)) if match else None

    @staticmethod
    def _extract_similar_to(query: str) -> str | None:
        match = re.search(r"similar to ([\w\s:.'-]+?)(?: but|,|\.|$)", query, flags=re.IGNORECASE)
        return match.group(1).strip() if match else None
