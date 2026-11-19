# smol-ui

A lightweight web UI for managing [smol-llm-proxy](https://github.com/robolamp/smol-llm-proxy) — per-user API keys, server routing, model aliases, and token usage tracking.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Features

- **Dashboard** — overview of keys, servers, and aliases at a glance
- **API Key Management** — create, revoke, toggle active, set RPM/TPM rate limits
- **Server Management** — register llama-server instances, assign/unassign models
- **Alias Management** — create short names that map to model names
- **Usage Tracking** — view token usage logs and summaries with date/key filters
- **Dark theme** — clean dark UI built with Tailwind CSS

## Quick Start

### Prerequisites

- Docker & Docker Compose (or Python 3.10+)

### Docker Compose

```bash
# 1. Clone & configure
cp .env.example .env
# Edit .env — set SMOL_PROXY_URL and optionally ADMIN_KEY

# 2. Run
docker compose up -d --build
```

Open [http://localhost:8080](http://localhost:8080)

### Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8080](http://localhost:8080)

## Configuration

| Variable | Default | Description |
|---|---|---|
| `SMOL_PROXY_URL` | `http://localhost:8000` | URL of your smol-llm-proxy instance |
| `ADMIN_KEY` | *(empty)* | Bearer token for proxy admin endpoints |
| `APP_PORT` | `8080` | Port the UI listens on |

## Architecture

```
[Browser] --> [smol-ui :8080] --> [smol-llm-proxy :8000]
              (FastAPI + Jinja2)    (llama.cpp proxy)
```

smol-ui acts as a thin proxy layer — all admin API calls are forwarded to smol-llm-proxy. The UI is a single-page application with server-rendered HTML templates and vanilla JavaScript.

## Admin API Endpoints

smol-ui exposes these API routes that forward to smol-llm-proxy:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/keys` | List API keys |
| POST | `/api/keys` | Create key |
| DELETE | `/api/keys/{id}` | Revoke key |
| PATCH | `/api/keys/{id}/toggle` | Activate/deactivate |
| PUT | `/api/keys/{id}/limits` | Set rate limits |
| GET | `/api/servers` | List servers |
| POST | `/api/servers` | Add server |
| DELETE | `/api/servers/{id}` | Remove server |
| POST | `/api/servers/{id}/models` | Assign model |
| DELETE | `/api/servers/{id}/models/{name}` | Unassign model |
| GET | `/api/aliases` | List aliases |
| POST | `/api/aliases` | Create alias |
| PATCH | `/api/aliases/{name}` | Update alias |
| DELETE | `/api/aliases/{name}` | Delete alias |
| GET | `/api/usage` | Usage logs |
| GET | `/api/usage/summary/real` | Usage summary |

## License

MIT

## Credits

This project uses [Charm Icons](https://github.com/jaynewey/charm-icons) (MIT License) by jaynewey for UI icons.

Icons used: `home`, `key`, `server`, `users`, `hash`, `cog`, `power`, `bin`, `plus`, `pencil`, `alert-circle`, `refresh`, `tick`, `cross`, `eye`, `calendar`, `menu`, `arrow-left`, `arrow-right`, `download-cloud`, `filter`, `play-circle`, `stop-circle`, `ellipsis`.
