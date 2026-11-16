"""FastAPI application factory."""

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="Stateside API", version="0.1.0")
    app.state.settings = settings
    app.include_router(health_router)
    return app


app = create_app()
