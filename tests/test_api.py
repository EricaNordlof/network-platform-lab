from pathlib import Path
import os
import sys

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "api"))
os.environ["CONFIG_ROOT"] = str(PROJECT_ROOT / "configs" / "frr")

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["config_root_exists"] is True


def test_topology_contains_two_sites() -> None:
    response = client.get("/topology")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["sites"]) == 2
    assert payload["transit_network"] == "10.255.0.0/29"
    assert {"BGP", "OSPF"} <= set(payload["routing_protocols"])


def test_routers() -> None:
    response = client.get("/routers")
    assert response.status_code == 200
    names = {router["name"] for router in response.json()}
    assert names == {"edge-malmo", "edge-london"}


def test_router_config_is_readable() -> None:
    response = client.get("/routers/edge-malmo/config")
    assert response.status_code == 200
    assert "router bgp 65001" in response.text
    assert "router ospf" in response.text


def test_path_traversal_is_rejected() -> None:
    response = client.get("/routers/..%2F..%2Fetc/config")
    assert response.status_code in {400, 404}
