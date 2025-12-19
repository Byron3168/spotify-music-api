import sqlite3
from typing import List, Optional
import os
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL", "./data/playlists.db")


def _conn():
    path = DATABASE_URL
    # if provided as sqlite:///... strip prefix
    if path.startswith("sqlite:///"):
        path = path.replace("sqlite:///", "")
    p = Path(path)
    if not p.parent.exists():
        p.parent.mkdir(parents=True)
    return sqlite3.connect(str(p))


def init_db():
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS playlists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            artists TEXT,
            playlist_id TEXT,
            FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    conn.close()


def list_playlists() -> List[dict]:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM playlists")
    rows = cur.fetchall()
    result = []
    for r in rows:
        pid, name, desc = r
        cur.execute("SELECT id, name, artists FROM tracks WHERE playlist_id = ?", (pid,))
        tracks = cur.fetchall()
        result.append({"id": pid, "name": name, "description": desc, "tracks": [{"id": t[0], "name": t[1], "artists": t[2].split(",") if t[2] else []} for t in tracks]})
    conn.close()
    return result


def get_playlist(pid: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM playlists WHERE id = ?", (pid,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return None
    pid, name, desc = r
    cur.execute("SELECT id, name, artists FROM tracks WHERE playlist_id = ?", (pid,))
    tracks = cur.fetchall()
    conn.close()
    return {"id": pid, "name": name, "description": desc, "tracks": [{"id": t[0], "name": t[1], "artists": t[2].split(",") if t[2] else []} for t in tracks]}


def create_playlist(obj: dict):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO playlists (id, name, description) VALUES (?, ?, ?)", (obj["id"], obj["name"], obj.get("description")))
    for t in obj.get("tracks", []):
        cur.execute("INSERT INTO tracks (id, name, artists, playlist_id) VALUES (?, ?, ?, ?)", (t["id"], t["name"], ",".join(t.get("artists", [])), obj["id"]))
    conn.commit()
    conn.close()


def update_playlist(pid: str, obj: dict):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM playlists WHERE id = ?", (pid,))
    if not cur.fetchone():
        conn.close()
        return None
    cur.execute("UPDATE playlists SET name = ?, description = ? WHERE id = ?", (obj["name"], obj.get("description"), pid))
    cur.execute("DELETE FROM tracks WHERE playlist_id = ?", (pid,))
    for t in obj.get("tracks", []):
        cur.execute("INSERT INTO tracks (id, name, artists, playlist_id) VALUES (?, ?, ?, ?)", (t["id"], t["name"], ",".join(t.get("artists", [])), pid))
    conn.commit()
    conn.close()


def delete_playlist(pid: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM playlists WHERE id = ?", (pid,))
    if not cur.fetchone():
        conn.close()
        return False
    cur.execute("DELETE FROM tracks WHERE playlist_id = ?", (pid,))
    cur.execute("DELETE FROM playlists WHERE id = ?", (pid,))
    conn.commit()
    conn.close()
    return True
