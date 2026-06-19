# GameMind

GameMind is a production-oriented AI game recommendation platform. It accepts natural language preferences like “I want a relaxing RPG with exploration and crafting,” retrieves grounded game candidates from ChromaDB, and ranks them with an OpenAI-backed recommendation agent or a deterministic local ranker for development and tests.

## Stack

- Python 3.12
- FastAPI
- LangChain tools
- OpenAI GPT and embedding APIs
- ChromaDB
- Docker
- Pytest

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
python scripts/generate_dataset.py --count 500
python scripts/ingest_games.py
uvicorn gamemind.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation.

## OpenAI Configuration

The default `.env.example` uses local deterministic embeddings and ranking so tests and demos work without credentials. For production OpenAI behavior:

```env
GAMEMIND_OPENAI_API_KEY=sk-...
GAMEMIND_USE_LOCAL_EMBEDDINGS=false
GAMEMIND_USE_LOCAL_RANKER=false
```

## API

- `POST /recommend`: returns ranked recommendations with metadata-grounded reasons.
- `GET /games`: lists sample game metadata with optional `genre` and `tag` filters.
- `GET /health`: service status and indexed game count.

See [docs/API.md](docs/API.md) for examples.

## Data Pipeline

`scripts/generate_dataset.py` creates a deterministic JSONL corpus with at least 500 games and fields:

- `title`
- `genre`
- `tags`
- `release_year`
- `rating`
- `description`

`scripts/ingest_games.py` embeds game metadata and stores vectors in ChromaDB.

## Agent Architecture

`gamemind/agents/tools.py` implements the LangChain tools:

- Preference Extraction Tool
- Genre Filtering Tool
- Similarity Search Tool
- Recommendation Ranking Tool

The recommendation service composes these capabilities into a RAG pipeline: extract preferences, retrieve with ChromaDB, rank candidates, and return grounded reasons.

## Evaluation

```bash
python scripts/evaluate.py --output evaluation_report.json
```

The report measures relevance, grounding, and coherence over representative queries.

## Tests

```bash
pytest
```

The test configuration enforces 90% minimum coverage.

## Docker

```bash
docker compose up --build
```

The image generates the sample dataset and ingests it into ChromaDB during build.
# AI-Game-Recommendation-System
