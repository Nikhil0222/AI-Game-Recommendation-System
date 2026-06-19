from __future__ import annotations

import random

from gamemind.domain.models import Game

GENRE_PROFILES: dict[str, dict[str, list[str]]] = {
    "RPG": {
        "tags": ["story-rich", "exploration", "crafting", "quests", "character progression"],
        "moods": ["immersive", "relaxing", "epic", "cozy"],
    },
    "Action Adventure": {
        "tags": ["combat", "open world", "puzzles", "cinematic", "boss fights"],
        "moods": ["exciting", "epic", "challenging"],
    },
    "Strategy": {
        "tags": ["turn-based", "management", "tactics", "base building", "economy"],
        "moods": ["thoughtful", "challenging", "focused"],
    },
    "Simulation": {
        "tags": ["sandbox", "management", "crafting", "cozy", "systems"],
        "moods": ["relaxing", "creative", "cozy"],
    },
    "Puzzle": {
        "tags": ["logic", "short sessions", "minimalist", "brain teaser", "casual"],
        "moods": ["calm", "focused", "relaxing"],
    },
    "Roguelike": {
        "tags": ["runs", "procedural", "high replayability", "build crafting", "indie"],
        "moods": ["challenging", "tense", "rewarding"],
    },
    "Platformer": {
        "tags": ["precision", "colorful", "short sessions", "collectibles", "indie"],
        "moods": ["playful", "casual", "challenging"],
    },
    "Narrative": {
        "tags": ["choices matter", "story-rich", "low combat", "atmospheric", "characters"],
        "moods": ["reflective", "emotional", "relaxing"],
    },
    "Survival": {
        "tags": ["crafting", "base building", "exploration", "resource management", "co-op"],
        "moods": ["tense", "immersive", "creative"],
    },
    "Sports": {
        "tags": ["competitive", "short sessions", "multiplayer", "skill-based", "casual"],
        "moods": ["energetic", "social", "casual"],
    },
}

TITLE_PREFIXES = [
    "Astral",
    "Verdant",
    "Iron",
    "Moonlit",
    "Pixel",
    "Silent",
    "Crimson",
    "Golden",
    "Arcane",
    "Neon",
    "Frost",
    "Solar",
    "Hidden",
    "Wild",
    "Clockwork",
    "Dream",
]

TITLE_NOUNS = [
    "Haven",
    "Frontier",
    "Odyssey",
    "Legends",
    "Valley",
    "Citadel",
    "Expedition",
    "Kingdoms",
    "Drift",
    "Chronicles",
    "Workshop",
    "Sanctuary",
    "Quest",
    "Tactics",
    "Harbor",
    "Run",
]


def generate_games(count: int = 500, seed: int = 42) -> list[Game]:
    rng = random.Random(seed)
    genres = list(GENRE_PROFILES)
    games: list[Game] = []

    for index in range(count):
        genre = genres[index % len(genres)]
        profile = GENRE_PROFILES[genre]
        prefix = TITLE_PREFIXES[index % len(TITLE_PREFIXES)]
        noun = TITLE_NOUNS[(index // len(TITLE_PREFIXES)) % len(TITLE_NOUNS)]
        title = f"{prefix} {noun} {index + 1:03d}"
        tags = rng.sample(profile["tags"], k=3)
        mood = rng.choice(profile["moods"])
        release_year = rng.randint(2005, 2026)
        rating = round(rng.uniform(3.2, 4.9), 1)
        session = rng.choice(["15-minute", "30-minute", "long-form", "weekend"])
        progression_style = rng.choice(["gentle", "deep", "snappy", "layered"])
        description = (
            f"A {mood} {genre.lower()} built around {tags[0]}, {tags[1]}, and {tags[2]}. "
            f"It supports {session} play with a {progression_style} "
            "progression loop and strong player agency."
        )
        games.append(
            Game(
                id=f"game-{index + 1:04d}",
                title=title,
                genre=genre,
                tags=tags + [mood, session],
                release_year=release_year,
                rating=rating,
                description=description,
            )
        )

    return games
