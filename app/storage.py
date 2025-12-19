import json
import os
from pathlib import Path
from typing import Dict, Any


PLAYLISTS_FILE = os.getenv("PLAYLISTS_FILE", "./data/playlists.json")


def _ensure_file():
    p = Path(PLAYLISTS_FILE)
    if not p.parent.exists():
        p.parent.mkdir(parents=True)
    if not p.exists():
        p.write_text(json.dumps({}))


def load_all() -> Dict[str, Any]:
    _ensure_file()
    with open(PLAYLISTS_FILE, "r") as fh:
        return json.load(fh)


def save_all(data: Dict[str, Any]):
    _ensure_file()
    with open(PLAYLISTS_FILE, "w") as fh:
        json.dump(data, fh, indent=2)
