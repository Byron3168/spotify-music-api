# Demo & Evidence

This file contains quick commands and sample outputs you can use as demo evidence or to take screenshots.

List playlists (public):

```bash
curl http://localhost:8000/api/v1/playlists
# => [] (empty list)
```

Create playlist (protected):

```bash
curl -X POST http://localhost:8000/api/v1/playlists \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: demo_api_key" \
  -d '{"name":"My List","tracks":[]}'
# => 201 Created with playlist JSON
```

Search:

```bash
curl "http://localhost:8000/api/v1/search?q=daft+punk"
# => {"query":"daft punk","results":[...]} (demo results when SPOTIFY creds missing)
```

Screenshots: When you run the commands above, take screenshots of the terminal (or browser OpenAPI page at `/docs`) and save them under `screenshots/` to include in your submission.
