from fastapi import FastAPI

from gamemind.api.routes import router
from gamemind.core.config import get_settings
from gamemind.core.errors import register_exception_handlers
from gamemind.core.logging import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(
        title="GameMind API",
        description=(
            "AI game recommendation platform using FastAPI, LangChain tools, OpenAI, and "
            "ChromaDB."
        ),
        version="0.1.0",
    )
    register_exception_handlers(app)
    app.include_router(router)
    return app


app = create_app()
