import os
import time
from typing import List, Dict
import requests


class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self._token = None
        self._token_expires = 0

    def _get_token(self):
        if self.client_id and self.client_secret and time.time() < self._token_expires:
            return self._token
        if not (self.client_id and self.client_secret):
            return None
        resp = requests.post(
            "https://accounts.spotify.com/api/token",
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_expires = time.time() + data.get("expires_in", 3600) - 60
        return self._token

    def search_tracks(self, query: str) -> List[Dict]:
        token = self._get_token()
        if not token:
            # Return mocked results when credentials not provided
            return [
                {"id": "mock1", "name": f"{query} (demo)", "artists": ["Demo Artist"]}
            ]
        resp = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            params={"q": query, "type": "track", "limit": 10},
        )
        resp.raise_for_status()
        items = resp.json().get("tracks", {}).get("items", [])
        return [
            {"id": it["id"], "name": it["name"], "artists": [a["name"] for a in it["artists"]]}
            for it in items
        ]
