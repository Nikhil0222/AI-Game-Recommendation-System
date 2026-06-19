from gamemind.agents.tools import GameMindTools


def test_langchain_tool_manifest(client) -> None:
    service = client.app.dependency_overrides.get("service")
    from gamemind.dependencies import get_recommendation_service

    game_tools = GameMindTools(service or get_recommendation_service())
    tools = game_tools.as_langchain_tools()
    names = {tool.name for tool in tools}
    assert "preference_extraction_tool" in names
    assert "genre_filtering_tool" in names
    assert "similarity_search_tool" in names
    assert "recommendation_ranking_tool" in names
    assert "preference_extraction_tool" in game_tools.tool_manifest_json()


def test_tool_methods_return_grounded_payloads(client) -> None:
    from gamemind.dependencies import get_recommendation_service

    game_tools = GameMindTools(get_recommendation_service())
    prefs = game_tools.preference_extraction("relaxing RPG crafting")
    assert prefs["genres"] == ["RPG"]

    genre_games = game_tools.genre_filtering("RPG", limit=2)
    assert len(genre_games) == 2
    assert all(game["genre"] == "RPG" for game in genre_games)

    search_results = game_tools.similarity_search("cozy crafting RPG", top_k=3)
    assert len(search_results) == 3
    ranked = game_tools.recommendation_ranking(
        "cozy crafting RPG",
        [item["game"]["id"] for item in search_results],
        top_k=2,
    )
    assert len(ranked) == 2
    assert ranked[0]["reason"]
