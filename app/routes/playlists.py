from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import uuid4

from app.models import Playlist, PlaylistCreate, Track
from app.auth import get_api_key
from app.services.spotify import SpotifyClient
from app import repository

# ensure backend initialized
repository.ensure_backend()

router = APIRouter()
spotify = SpotifyClient()


@router.get("/playlists", response_model=List[Playlist])
def list_playlists():
    data = repository.list_playlists()
    return [Playlist(**p) for p in data]


@router.get("/playlists/{playlist_id}", response_model=Playlist)
def get_playlist(playlist_id: str):
    p = repository.get_playlist(playlist_id)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Playlist(**p)


@router.post("/playlists", response_model=Playlist, status_code=status.HTTP_201_CREATED)
def create_playlist(payload: PlaylistCreate, api_key: str = Depends(get_api_key)):
    pid = str(uuid4())
    obj = {"id": pid, "name": payload.name, "description": payload.description, "tracks": [t.dict() for t in payload.tracks]}
    repository.create_playlist(obj)
    return Playlist(**obj)


@router.put("/playlists/{playlist_id}", response_model=Playlist)
def update_playlist(playlist_id: str, payload: PlaylistCreate, api_key: str = Depends(get_api_key)):
    existing = repository.get_playlist(playlist_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    obj = {"id": playlist_id, "name": payload.name, "description": payload.description, "tracks": [t.dict() for t in payload.tracks]}
    repository.update_playlist(playlist_id, obj)
    return Playlist(**obj)


@router.delete("/playlists/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(playlist_id: str, api_key: str = Depends(get_api_key)):
    ok = repository.delete_playlist(playlist_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return None


@router.get("/search")
def search(q: str):
    results = spotify.search_tracks(q)
    return {"query": q, "results": results}
