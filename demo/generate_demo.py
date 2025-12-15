from pathlib import Path
import json
import sys
from pathlib import Path as P
sys.path.append(str(P(__file__).resolve().parents[1]))
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

from app.main import app
from fastapi.testclient import TestClient


OUT = Path("screenshots")
OUT.mkdir(exist_ok=True)


def save_text_png(text: str, path: Path):
    if PIL_AVAILABLE:
        # basic text -> PNG
        font = ImageFont.load_default()
        lines = text.splitlines() or [""]
        width = max(font.getsize(line)[0] for line in lines) + 20
        height = (font.getsize(lines[0])[1] + 4) * len(lines) + 20
        img = Image.new("RGB", (max(width, 300), max(height, 100)), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        y = 10
        for line in lines:
            d.text((10, y), line, fill=(0, 0, 0), font=font)
            y += font.getsize(line)[1] + 4
        img.save(path)
    else:
        # fallback: save text file and a tiny placeholder PNG
        text_path = path.with_suffix(".txt")
        text_path.write_text(text)
        # write a 1x1 white PNG
        import base64
        png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
        path.write_bytes(base64.b64decode(png_b64))


def run():
    client = TestClient(app)

    # health
    h = client.get("/health")
    text = f"GET /health\n\n{json.dumps(h.json(), indent=2)}"
    save_text_png(text, OUT / "health.png")

    # list playlists
    ls = client.get("/api/v1/playlists")
    text = f"GET /api/v1/playlists\n\nStatus: {ls.status_code}\n{json.dumps(ls.json(), indent=2)}"
    save_text_png(text, OUT / "list_playlists.png")

    # protected create (should fail without key)
    create = client.post("/api/v1/playlists", json={"name": "Demo", "tracks": []})
    text = f"POST /api/v1/playlists (no key)\n\nStatus: {create.status_code}\n{create.text}"
    save_text_png(text, OUT / "create_unauthorized.png")

    # create with demo key
    create2 = client.post("/api/v1/playlists", json={"name": "Demo", "tracks": []}, headers={"X-API-KEY": "demo_api_key"})
    text = f"POST /api/v1/playlists (with key)\n\nStatus: {create2.status_code}\n{json.dumps(create2.json(), indent=2)}"
    save_text_png(text, OUT / "create_authorized.png")

    # search
    s = client.get("/api/v1/search?q=daft+punk")
    text = f"GET /api/v1/search?q=daft+punk\n\nStatus: {s.status_code}\n{json.dumps(s.json(), indent=2)}"
    save_text_png(text, OUT / "search.png")


if __name__ == "__main__":
    run()
