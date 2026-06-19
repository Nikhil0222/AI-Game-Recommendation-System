FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY gamemind ./gamemind
COPY scripts ./scripts
COPY data ./data
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[dev]"
RUN python scripts/generate_dataset.py --output data/sample_games.jsonl --count 500 \
    && python scripts/ingest_games.py --dataset data/sample_games.jsonl --chroma-path .chroma
EXPOSE 8000
CMD ["uvicorn", "gamemind.main:app", "--host", "0.0.0.0", "--port", "8000"]
