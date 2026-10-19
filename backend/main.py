"""FastAPI entrypoint: uvicorn backend.main:app --reload."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.predict import router

app = FastAPI(title="Real Estate AI API", version="1.0.0", description="House-price prediction service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api/v1", tags=["predictions"])


@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {"status": "ok"}
