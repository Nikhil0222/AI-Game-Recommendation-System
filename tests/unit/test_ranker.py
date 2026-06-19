from gamemind.data.synthetic import generate_games
from gamemind.domain.models import Preferences, SearchResult
from gamemind.services.ranker import LocalRecommendationRanker


def test_ranker_promotes_matching_preferences() -> None:
    games = generate_games(20)
    candidates = [SearchResult(game=game, score=0.5) for game in games]
    prefs = Preferences(raw_query="relaxing RPG crafting", genres=["RPG"], tags=["crafting"])
    ranked = LocalRecommendationRanker().rank("relaxing RPG crafting", prefs, candidates, top_k=3)
    assert len(ranked) == 3
    assert ranked[0].game.genre == "RPG"
    assert "recommended because" in ranked[0].reason
