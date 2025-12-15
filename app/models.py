from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Track(BaseModel):
    id: str
    name: str
    artists: List[str] = []


class PlaylistBase(BaseModel):
    name: str = Field(..., example="Chill Vibes")
    description: Optional[str] = None


class PlaylistCreate(PlaylistBase):
    tracks: List[Track] = []


class Playlist(PlaylistBase):
    id: UUID
    tracks: List[Track] = []

    class Config:
        orm_mode = True
