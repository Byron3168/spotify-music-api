"""Migrate playlists from JSON storage to SQLite using repository API.

Usage: python scripts/migrate_playlists.py
"""
import json
from app import storage, repository
from pathlib import Path


def main():
    src = Path(storage.PLAYLISTS_FILE)
    if not src.exists():
        print("No JSON playlists file found at", src)
        return
    data = storage.load_all()
    if not data:
        print("No playlists to migrate")
        return
    repository.ensure_backend()
    for pid, obj in data.items():
        print("Migrating", pid)
        repository.create_playlist(obj)
    print("Migration complete")


if __name__ == "__main__":
    main()
