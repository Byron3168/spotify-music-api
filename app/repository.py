import os
from typing import Dict, Any
from app import storage
from app import db


USE_SQLITE = os.getenv("USE_SQLITE", "1") in ["1", "true", "True"]


def ensure_backend():
    if USE_SQLITE:
        db.init_db()


def list_playlists():
    if USE_SQLITE:
        return db.list_playlists()
    return list(storage.load_all().values())


def get_playlist(pid: str):
    if USE_SQLITE:
        return db.get_playlist(pid)
    data = storage.load_all()
    return data.get(pid)


def create_playlist(obj: Dict[str, Any]):
    if USE_SQLITE:
        return db.create_playlist(obj)
    data = storage.load_all()
    data[obj["id"]] = obj
    storage.save_all(data)


def update_playlist(pid: str, obj: Dict[str, Any]):
    if USE_SQLITE:
        return db.update_playlist(pid, obj)
    data = storage.load_all()
    data[pid] = obj
    storage.save_all(data)


def delete_playlist(pid: str):
    if USE_SQLITE:
        return db.delete_playlist(pid)
    data = storage.load_all()
    if pid in data:
        del data[pid]
        storage.save_all(data)
        return True
    return False
