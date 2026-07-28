from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel

APP_STARTED = time.time()
REQUESTS = Counter(
    "network_platform_api_requests_total",
    "Number of requests handled by endpoint",
    ["endpoint"],
)
ROUTERS_CONFIGURED = Gauge(
    "network_platform_routers_configured",
    "Number of router configuration directories detected",
)

CONFIG_ROOT = Path(os.getenv("CONFIG_ROOT", "/workspace/configs/frr")).resolve()

app = FastAPI(
    title="Network Platform API",
    description="Read-only self-service API for a local network engineering portfolio lab.",
    version="1.0.0",
)


class RouterSummary(BaseModel):
    name: str
    config_available: bool
    daemons_available: bool


def _router_path(router_name: str) -> Path:
    if not router_name.replace("-", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid router name")

    candidate = (CONFIG_ROOT / router_name).resolve()
    if CONFIG_ROOT not in candidate.parents:
        raise HTTPException(status_code=400, detail="Invalid router path")
    if not candidate.exists() or not candidate.is_dir():
        raise HTTPException(status_code=404, detail="Router not found")
    return candidate


def _routers() -> list[RouterSummary]:
    if not CONFIG_ROOT.exists():
        return []

    result = []
    for path in sorted(CONFIG_ROOT.iterdir()):
        if not path.is_dir():
            continue
        result.append(
            RouterSummary(
                name=path.name,
                config_available=(path / "frr.conf").is_file(),
                daemons_available=(path / "daemons").is_file(),
            )
        )
    ROUTERS_CONFIGURED.set(len(result))
    return result


@app.get("/health")
def health() -> dict[str, Any]:
    REQUESTS.labels(endpoint="/health").inc()
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - APP_STARTED, 2),
        "config_root_exists": CONFIG_ROOT.exists(),
    }


@app.get("/topology")
def topology() -> dict[str, Any]:
    REQUESTS.labels(endpoint="/topology").inc()
    return {
        "sites": [
            {
                "name": "malmo",
                "asn": 65001,
                "router": "edge-malmo",
                "site_network": "10.10.1.0/24",
            },
            {
                "name": "london",
                "asn": 65002,
                "router": "edge-london",
                "site_network": "10.20.1.0/24",
            },
        ],
        "transit_network": "10.255.0.0/30",
        "routing_protocols": ["BGP", "OSPF"],
    }


@app.get("/routers", response_model=list[RouterSummary])
def routers() -> list[RouterSummary]:
    REQUESTS.labels(endpoint="/routers").inc()
    return _routers()


@app.get("/routers/{router_name}", response_model=RouterSummary)
def router(router_name: str) -> RouterSummary:
    REQUESTS.labels(endpoint="/routers/{router_name}").inc()
    path = _router_path(router_name)
    return RouterSummary(
        name=path.name,
        config_available=(path / "frr.conf").is_file(),
        daemons_available=(path / "daemons").is_file(),
    )


@app.get("/routers/{router_name}/config", response_class=PlainTextResponse)
def router_config(router_name: str) -> str:
    REQUESTS.labels(endpoint="/routers/{router_name}/config").inc()
    path = _router_path(router_name) / "frr.conf"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Configuration not found")
    return path.read_text(encoding="utf-8")


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    REQUESTS.labels(endpoint="/metrics").inc()
    _routers()
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
