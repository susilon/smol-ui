from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from urllib.parse import urljoin
import httpx
import os

app = FastAPI(title="smol-ui - smol-llm-proxy Manager")

PROXY_URL = os.getenv("SMOL_PROXY_URL", "http://localhost:8000")
ADMIN_KEY = os.getenv("ADMIN_KEY", "")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_admin_headers():
    if ADMIN_KEY:
        return {"Authorization": f"Bearer {ADMIN_KEY}"}
    return {}


# ── Page Routes ──────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/keys", response_class=HTMLResponse)
async def keys_page(request: Request):
    return templates.TemplateResponse("keys.html", {"request": request})


@app.get("/servers", response_class=HTMLResponse)
async def servers_page(request: Request):
    return templates.TemplateResponse("servers.html", {"request": request})


@app.get("/aliases", response_class=HTMLResponse)
async def aliases_page(request: Request):
    return templates.TemplateResponse("aliases.html", {"request": request})


@app.get("/usage", response_class=HTMLResponse)
async def usage_page(request: Request):
    return templates.TemplateResponse("usage.html", {"request": request})


# ── API Proxy Routes ─────────────────────────────────────────

async def proxy_request(method: str, path: str, params: dict = None, body: dict = None):
    url = urljoin(PROXY_URL, path)
    headers = {"Content-Type": "application/json"}
    if ADMIN_KEY:
        headers["Authorization"] = f"Bearer {ADMIN_KEY}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                resp = await client.get(url, params=params, headers=headers)
            elif method == "POST":
                resp = await client.post(url, json=body, params=params, headers=headers)
            elif method == "PUT":
                resp = await client.put(url, json=body, params=params, headers=headers)
            elif method == "PATCH":
                resp = await client.patch(url, json=body, params=params, headers=headers)
            elif method == "DELETE":
                resp = await client.delete(url, params=params, headers=headers)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            resp.raise_for_status()
            text = resp.text.strip()
            if not text:
                return {}
            return resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Cannot connect to smol-llm-proxy. Check SMOL_PROXY_URL.")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Proxy error: {str(e)}")


# ── Keys API ──────────────────────────────────────────────────

@app.get("/api/keys")
async def api_get_keys():
    return await proxy_request("GET", "/admin/keys")


@app.post("/api/keys")
async def api_create_key(request: Request):
    body = await request.json()
    return await proxy_request("POST", "/admin/keys", body=body)


@app.delete("/api/keys/{key_id}")
async def api_delete_key(key_id: int):
    return await proxy_request("DELETE", f"/admin/keys/{key_id}")


@app.patch("/api/keys/{key_id}/toggle")
async def api_toggle_key(key_id: int):
    return await proxy_request("PATCH", f"/admin/keys/{key_id}/toggle")


@app.put("/api/keys/{key_id}/limits")
async def api_update_limits(key_id: int, request: Request):
    body = await request.json()
    return await proxy_request("PUT", f"/admin/keys/{key_id}/limits", body=body)


# ── Servers API ───────────────────────────────────────────────

@app.get("/api/servers")
async def api_get_servers():
    return await proxy_request("GET", "/admin/servers")


@app.post("/api/servers")
async def api_create_server(request: Request):
    body = await request.json()
    return await proxy_request("POST", "/admin/servers", body=body)


@app.delete("/api/servers/{server_id}")
async def api_delete_server(server_id: int):
    return await proxy_request("DELETE", f"/admin/servers/{server_id}")


@app.patch("/api/servers/{server_id}")
async def api_update_server(server_id: int, request: Request):
    body = await request.json()
    return await proxy_request("PATCH", f"/admin/servers/{server_id}", body=body)


@app.post("/api/servers/{server_id}/models")
async def api_assign_model(server_id: int, request: Request):
    body = await request.json()
    reassign = Query(False)
    return await proxy_request("POST", f"/admin/servers/{server_id}/models", params={"reassign": reassign}, body=body)


@app.delete("/api/servers/{server_id}/models/{model_name}")
async def api_unassign_model(server_id: int, model_name: str):
    return await proxy_request("DELETE", f"/admin/servers/{server_id}/models/{model_name}")


# ── Aliases API ───────────────────────────────────────────────

@app.get("/api/aliases")
async def api_get_aliases():
    return await proxy_request("GET", "/admin/aliases")


@app.post("/api/aliases")
async def api_create_alias(request: Request):
    body = await request.json()
    return await proxy_request("POST", "/admin/aliases", body=body)


@app.patch("/api/aliases/{alias_name}")
async def api_update_alias(alias_name: str, request: Request):
    body = await request.json()
    return await proxy_request("PATCH", f"/admin/aliases/{alias_name}", body=body)


@app.delete("/api/aliases/{alias_name}")
async def api_delete_alias(alias_name: str):
    return await proxy_request("DELETE", f"/admin/aliases/{alias_name}")


# ── Usage API ─────────────────────────────────────────────────

@app.get("/api/usage")
async def api_get_usage(
    key_id: Optional[int] = None,
    server_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    params = {k: v for k, v in {
        "key_id": key_id,
        "server_id": server_id,
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "offset": offset,
    }.items() if v is not None}
    return await proxy_request("GET", "/admin/usage", params=params)


@app.get("/api/usage/summary/real")
async def api_get_usage_summary(
    key_id: Optional[int] = None,
    server_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    params = {k: v for k, v in {
        "key_id": key_id,
        "server_id": server_id,
        "start_date": start_date,
        "end_date": end_date,
    }.items() if v is not None}
    return await proxy_request("GET", "/admin/usage/summary/real", params=params)
