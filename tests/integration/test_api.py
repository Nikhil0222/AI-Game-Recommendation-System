def test_health_endpoint(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_games_endpoint(client) -> None:
    response = client.get("/games?limit=5")
    payload = response.json()
    assert response.status_code == 200
    assert payload["count"] == 60
    assert len(payload["games"]) == 5


def test_recommend_endpoint(client) -> None:
    response = client.post(
        "/recommend",
        json={"query": "I want a relaxing RPG with crafting", "top_k": 3},
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["query"] == "I want a relaxing RPG with crafting"
    assert len(payload["recommendations"]) == 3
    assert all(item["reason"] for item in payload["recommendations"])
