# app/main.py
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestContextMiddleware
from app.api.v1.endpoints import router as api_v1_router

logger = setup_logging(settings.LOG_LEVEL)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.4.0",
    openapi_tags=[{"name": "Prédiction de trafic", "description": "API de prédiction + carte + heure de départ."}],
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

UI_DIR = Path(__file__).parent / "ui"
INDEX_PATH = UI_DIR / "index.html"

@app.get("/", include_in_schema=False)
async def servir_ui():
    return FileResponse(INDEX_PATH)
