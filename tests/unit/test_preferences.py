from gamemind.services.preferences import PreferenceExtractor


def test_extracts_genre_tags_and_time_budget() -> None:
    prefs = PreferenceExtractor().extract("I only have 30 minutes for a relaxing RPG with crafting")
    assert prefs.time_budget_minutes == 30
    assert "RPG" in prefs.genres
    assert "crafting" in prefs.tags
    assert prefs.mood == "relaxing"


def test_extracts_similarity_target() -> None:
    prefs = PreferenceExtractor().extract(
        "Recommend games similar to Witcher 3 but less combat focused."
    )
    assert prefs.similar_to == "Witcher 3"
    assert "Simulation" not in prefs.genres
    assert "low combat" in prefs.tags
    assert "story-rich" in prefs.tags
