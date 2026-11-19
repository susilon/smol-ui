# smol-ui

## Development

- **Stack:** Python + FastAPI + Jinja2 templates + vanilla JS + Tailwind CSS (CDN)
- **Run locally:** `pip install -r requirements.txt && uvicorn app.main:app --reload`
- **Port:** UI serves on port 8080 (configurable via `APP_PORT`)

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `SMOL_PROXY_URL` | `http://localhost:8000` | smol-llm-proxy base URL |
| `ADMIN_KEY` | *(empty)* | Admin bearer token for proxy |
| `APP_PORT` | `8080` | UI listen port |

## Project Structure

```
app/
  main.py              # FastAPI app + API proxy routes
  templates/           # Jinja2 HTML templates
    base.html          # Layout with sidebar nav
    index.html         # Dashboard
    keys.html          # API key management
    servers.html       # Server & model management
    aliases.html       # Alias management
    usage.html         # Usage logs & summaries
  static/js/
    app.js             # Shared JS (toasts, modals, nav)
requirements.txt
Dockerfile
docker-compose.yml
.env.example
```

## API Routes

All pages proxy to smol-llm-proxy admin endpoints:

- `GET /api/keys` — list/create keys
- `GET /api/servers` — list servers
- `GET /api/aliases` — list aliases
- `GET /api/usage` — usage logs
- `GET /api/usage/summary/real` — usage summary
