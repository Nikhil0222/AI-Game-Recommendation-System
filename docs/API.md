# GameMind API

GameMind exposes three REST endpoints.

## `GET /health`

Returns service status and the current ChromaDB collection count.

```json
{
  "status": "ok",
  "version": "0.1.0",
  "indexed_games": 500
}
```

## `GET /games`

Query parameters:

- `limit`: 1-500, default 100
- `offset`: default 0
- `genre`: optional exact genre filter
- `tag`: optional tag filter

## `POST /recommend`

Request:

```json
{
  "query": "I want a relaxing RPG",
  "top_k": 5
}
```

Response:

```json
{
  "query": "I want a relaxing RPG",
  "recommendations": [
    {
      "title": "Astral Haven 001",
      "genre": "RPG",
      "tags": ["exploration", "crafting", "quests", "relaxing", "30-minute"],
      "release_year": 2021,
      "rating": 4.5,
      "score": 0.81,
      "reason": "Astral Haven 001 is recommended because it matches the requested RPG genre and aligns on relaxing."
    }
  ]
}
```
