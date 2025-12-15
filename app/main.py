from fastapi import FastAPI
from app.routes.playlists import router as playlists_router

app = FastAPI(title="Music Discovery API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(playlists_router, prefix="/api/v1")
