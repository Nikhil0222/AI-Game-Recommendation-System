from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse

from gamemind import __version__
from gamemind.core.config import get_settings
from gamemind.dependencies import get_recommendation_service, get_repository
from gamemind.schemas import (
    GameItem,
    GamesResponse,
    HealthResponse,
    RecommendationItem,
    RecommendationResponse,
    RecommendRequest,
)
from gamemind.services.game_repository import GameRepository
from gamemind.services.recommendation import RecommendationService

router = APIRouter()
RecommendationServiceDep = Annotated[RecommendationService, Depends(get_recommendation_service)]
RepositoryDep = Annotated[GameRepository, Depends(get_repository)]


@router.get("/health", response_model=HealthResponse)
def health(service: RecommendationServiceDep) -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=__version__,
        indexed_games=service.vector_store.count(),
    )


@router.get("/games", response_model=GamesResponse)
def list_games(
    repository: RepositoryDep,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    genre: str | None = None,
    tag: str | None = None,
) -> GamesResponse:
    games = repository.list_games(limit=limit, offset=offset, genre=genre, tag=tag)
    return GamesResponse(
        count=repository.count(),
        games=[GameItem(**game.model_dump()) for game in games],
    )


@router.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>GameMind</title>
        <style>
            :root {
                color-scheme: dark;
                font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #0b1120;
                color: #e8eefb;
                text-rendering: optimizeLegibility;
            }
            * { box-sizing: border-box; }
            body { margin: 0; min-height: 100vh; background: radial-gradient(circle at top, rgba(56, 189, 248, 0.14), transparent 28%), linear-gradient(180deg, #020617 0%, #0b1120 100%); }
            a { color: #7dd3fc; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .page { width: min(1160px, calc(100% - 2rem)); margin: 0 auto; padding: 3rem 0 4rem; }
            .header { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; margin-bottom: 2rem; }
            .brand { display: flex; align-items: center; gap: 0.85rem; }
            .brand-mark { width: 48px; height: 48px; border-radius: 16px; background: linear-gradient(135deg, #34d399, #60a5fa); display: grid; place-items: center; color: #020617; font-weight: 700; }
            .brand-title { margin: 0; font-size: 1.5rem; letter-spacing: -0.05em; }
            .brand-subtitle { margin: 0.25rem 0 0; color: #94a3b8; font-size: 0.95rem; }
            .hero { display: grid; gap: 1.25rem; padding: 2.5rem 1.5rem; border-radius: 1.75rem; background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(148, 163, 184, 0.12); box-shadow: 0 35px 120px rgba(15, 23, 42, 0.28); }
            .hero h1 { margin: 0; font-size: clamp(2.75rem, 5vw, 4.5rem); line-height: 0.95; letter-spacing: -0.05em; }
            .hero p { margin: 0; max-width: 760px; color: #cbd5e1; font-size: 1.1rem; line-height: 1.8; }
            .layout { display: grid; gap: 1.5rem; grid-template-columns: minmax(0, 1.4fr) minmax(320px, 0.9fr); margin-top: 2rem; }
            .panel { background: rgba(15, 23, 42, 0.95); border-radius: 1.5rem; border: 1px solid rgba(148, 163, 184, 0.1); overflow: hidden; }
            .panel-body { padding: 1.75rem; }
            .panel-heading { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 1.5rem 1.75rem 0; }
            .panel-heading h2 { margin: 0; font-size: 1.2rem; }
            .panel-heading span { color: #94a3b8; font-size: 0.95rem; }
            .field { margin-bottom: 1.15rem; }
            .field label { display: block; margin-bottom: 0.65rem; font-weight: 700; color: #cbd5e1; }
            textarea, input[type="number"] { width: 100%; border-radius: 1rem; border: 1px solid rgba(148, 163, 184, 0.16); background: #0f172a; color: #f8fafc; padding: 1rem 1.1rem; font-size: 1rem; outline: none; transition: border-color 0.2s ease, box-shadow 0.2s ease; }
            textarea { min-height: 170px; resize: vertical; }
            textarea:focus, input[type="number"]:focus { border-color: #60a5fa; box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12); }
            .controls { display: grid; gap: 1rem; grid-template-columns: 1fr auto; align-items: center; }
            .controls input[type="number"] { max-width: 140px; }
            .button-primary { display: inline-flex; align-items: center; justify-content: center; gap: 0.55rem; background: linear-gradient(135deg, #38bdf8, #22d3ee); color: #020617; border: none; border-radius: 999px; font-weight: 700; padding: 1rem 1.5rem; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; }
            .button-primary:hover { transform: translateY(-2px); box-shadow: 0 18px 40px rgba(34, 211, 238, 0.24); }
            .button-primary:disabled { opacity: 0.65; cursor: not-allowed; transform: none; box-shadow: none; }
            .status { color: #94a3b8; font-size: 0.95rem; min-height: 1.35rem; }
            .badges { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.8rem; }
            .badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.5rem 0.8rem; border-radius: 999px; background: rgba(71, 85, 105, 0.18); color: #e2e8f0; font-size: 0.9rem; }
            .badge span { width: 8px; height: 8px; border-radius: 50%; background: #34d399; }
            .examples { display: grid; gap: 0.8rem; margin-top: 1rem; }
            .example { border-radius: 1rem; background: #111827; border: 1px solid rgba(148, 163, 184, 0.12); padding: 0.95rem 1rem; cursor: pointer; transition: background 0.2s ease; }
            .example:hover { background: rgba(56, 189, 248, 0.08); }
            .section-title { color: #e2e8f0; margin: 0 0 1rem; font-size: 1rem; letter-spacing: 0.01em; }
            .results { display: grid; gap: 1rem; }
            .recommendation { background: rgba(15, 23, 42, 0.98); border: 1px solid rgba(148, 163, 184, 0.12); border-radius: 1.4rem; padding: 1.6rem; box-shadow: 0 20px 50px rgba(15, 23, 42, 0.18); }
            .recommendation h3 { margin: 0 0 0.55rem; font-size: 1.2rem; }
            .recommendation .meta { margin-bottom: 0.9rem; color: #94a3b8; font-size: 0.95rem; }
            .recommendation p { margin: 0; line-height: 1.85; color: #cbd5e1; }
            .recommendation .tags { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 1rem; }
            .tags span { background: rgba(56, 189, 248, 0.12); color: #bae6fd; padding: 0.45rem 0.8rem; border-radius: 999px; font-size: 0.9rem; }
            .hero-grid { display: grid; gap: 1.5rem; grid-template-columns: minmax(0, 1fr) minmax(280px, 360px); align-items: center; }
            .metrics { display: grid; gap: 1rem; }
            .metric-card { background: rgba(15, 23, 42, 0.95); padding: 1.2rem 1.3rem; border-radius: 1.2rem; border: 1px solid rgba(148, 163, 184, 0.08); }
            .metric-card strong { display: block; color: #f8fafc; font-size: 1.5rem; }
            .metric-card span { color: #94a3b8; font-size: 0.95rem; }
            .footer { text-align: center; margin-top: 3rem; color: #94a3b8; font-size: 0.95rem; }
            .footer a { color: #38bdf8; }
            @media (max-width: 900px) {
                .layout, .hero-grid { grid-template-columns: 1fr; }
                .panel-heading { flex-direction: column; align-items: flex-start; }
            }
        </style>
    </head>
    <body>
        <main class="page">
            <header class="header">
                <div class="brand">
                    <div class="brand-mark">GM</div>
                    <div>
                        <h1 class="brand-title">GameMind</h1>
                        <p class="brand-subtitle">AI-driven game recommendations with grounding, transparency, and fine-tuned preference understanding.</p>
                    </div>
                </div>
                <div class="badges">
                    <span class="badge"><span></span>FastAPI</span>
                    <span class="badge"><span></span>ChromaDB</span>
                    <span class="badge"><span></span>Local & OpenAI Ready</span>
                </div>
            </header>

            <section class="hero">
                <div class="hero-grid">
                    <div>
                        <h1>Discover your next favorite game in seconds.</h1>
                        <p>Use natural language preferences to generate ranked, grounded recommendations with metadata-aware scoring, genre filtering, and optional OpenAI ranking.</p>
                    </div>
                    <div class="metrics">
                        <div class="metric-card"><strong>500+</strong><span>Example games</span></div>
                        <div class="metric-card"><strong>90%+</strong><span>Test coverage enforced</span></div>
                        <div class="metric-card"><strong>Realtime</strong><span>Fast recommendation API</span></div>
                    </div>
                </div>
            </section>

            <div class="layout">
                <section class="panel">
                    <div class="panel-heading">
                        <div>
                            <h2>Recommendation Builder</h2>
                            <span>Enter your gaming preference and get ranked suggestions.</span>
                        </div>
                        <div class="badge">Production Ready</div>
                    </div>
                    <div class="panel-body">
                        <div class="field">
                            <label for="query">What are you in the mood for?</label>
                            <textarea id="query" placeholder="e.g. A cozy crafting RPG with open-world exploration, low combat, and short sessions."></textarea>
                        </div>
                        <div class="field">
                            <label for="top_k">Recommendations to return</label>
                            <input id="top_k" type="number" min="1" max="10" value="5" />
                        </div>
                        <div class="controls">
                            <button id="recommend" class="button-primary">Generate recommendations</button>
                            <div class="status" id="status">Service status: checking…</div>
                        </div>
                        <div class="section-title">Example prompts</div>
                        <div class="examples">
                            <div class="example" data-value="A relaxing RPG with crafting, exploration, and low combat.">Relieving RPG with low combat</div>
                            <div class="example" data-value="A story-rich open world adventure with meaningful choices and exploration.">Story-driven open world adventure</div>
                            <div class="example" data-value="A quick, casual simulation game for short daily play sessions.">Short casual simulation</div>
                        </div>
                    </div>
                </section>

                <section class="panel">
                    <div class="panel-heading">
                        <h2>Recommendations</h2>
                        <span>Fast, grounded insights from the GameMind API.</span>
                    </div>
                    <div class="panel-body">
                        <div id="results" class="results"></div>
                        <div class="status" style="margin-top:1rem;">Use a prompt to fill this panel with ranked recommendations.</div>
                    </div>
                </section>
            </div>

            <footer class="footer">Powered by <a href="/docs">GameMind API docs</a>. For production OpenAI ranking, configure <code>GAMEMIND_USE_LOCAL_RANKER=false</code> and <code>GAMEMIND_OPENAI_API_KEY</code>.</footer>
        </main>

        <script>
            const queryInput = document.getElementById('query');
            const topKInput = document.getElementById('top_k');
            const recommendButton = document.getElementById('recommend');
            const resultsEl = document.getElementById('results');
            const statusEl = document.getElementById('status');
            const examples = Array.from(document.querySelectorAll('.example'));

            function setStatus(text, isError = false) {
                statusEl.textContent = text;
                statusEl.style.color = isError ? '#fda4af' : '#94a3b8';
            }

            async function updateHealth() {
                try {
                    const response = await fetch('/health');
                    if (!response.ok) throw new Error('health check failed');
                    const payload = await response.json();
                    setStatus(`Service online · v${payload.version} · indexed ${payload.indexed_games} games`);
                } catch (error) {
                    setStatus('Service unavailable. Please check API status.', true);
                }
            }

            async function recommend() {
                const query = queryInput.value.trim();
                const top_k = Math.max(1, Math.min(10, parseInt(topKInput.value, 10) || 5));
                if (!query) {
                    setStatus('Please enter a preference to continue.', true);
                    return;
                }
                recommendButton.disabled = true;
                recommendButton.textContent = 'Generating...';
                setStatus('Fetching recommendations...');
                resultsEl.innerHTML = '';
                try {
                    const response = await fetch('/recommend', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query, top_k }),
                    });
                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(errorText || `API error: ${response.status}`);
                    }
                    const payload = await response.json();
                    if (!payload.recommendations?.length) {
                        setStatus('No recommendations found. Try a different prompt.', true);
                        return;
                    }
                    setStatus(`Showing ${payload.recommendations.length} recommendations.`);
                    resultsEl.innerHTML = payload.recommendations.map(item => `
                        <article class="recommendation">
                            <h3>${item.title}</h3>
                            <div class="meta">${item.genre} · ${item.release_year} · Rating: ${item.rating} · Score: ${item.score.toFixed(2)}</div>
                            <p>${item.reason}</p>
                            <div class="tags">${item.tags.map(tag => `<span>${tag}</span>`).join('')}</div>
                        </article>
                    `).join('');
                } catch (error) {
                    console.error(error);
                    setStatus('Unable to load recommendations. Please try again later.', true);
                } finally {
                    recommendButton.disabled = false;
                    recommendButton.textContent = 'Generate recommendations';
                }
            }

            examples.forEach(example => {
                example.addEventListener('click', () => {
                    queryInput.value = example.dataset.value;
                    recommend();
                });
            });

            recommendButton.addEventListener('click', recommend);
            queryInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' && event.ctrlKey) recommend();
            });
            window.addEventListener('load', updateHealth);
        </script>
    </body>
    </html>
    """


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(
    request: RecommendRequest,
    service: RecommendationServiceDep,
) -> RecommendationResponse:
    settings = get_settings()
    top_k = request.top_k or settings.default_recommendation_count
    top_k = min(top_k, settings.max_recommendation_count)
    recommendations = service.recommend(request.query, top_k=top_k)
    return RecommendationResponse(
        query=request.query,
        recommendations=[
            RecommendationItem(
                title=item.game.title,
                genre=item.game.genre,
                tags=item.game.tags,
                release_year=item.game.release_year,
                rating=item.game.rating,
                score=item.score,
                reason=item.reason,
            )
            for item in recommendations
        ],
    )
