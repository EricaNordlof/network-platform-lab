from ipaddress import ip_address, ip_network
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = PROJECT_ROOT / "docker-compose.yml"

EXPECTED_SERVICES = {
    "api",
    "edge-malmo",
    "edge-london",
    "app-malmo",
    "app-london",
    "prometheus",
    "blackbox",
    "grafana",
}

EXPECTED_SUBNETS = {
    "management": "172.30.0.0/24",
    "transit": "10.255.0.0/29",
    "malmo": "10.10.1.0/24",
    "london": "10.20.1.0/24",
}


def _compose() -> dict[str, Any]:
    with COMPOSE_FILE.open(encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    assert isinstance(document, dict)
    return document


def test_compose_defines_all_documented_services() -> None:
    services = _compose().get("services")

    assert isinstance(services, dict)
    assert set(services) == EXPECTED_SERVICES


def test_compose_network_addresses_match_declared_subnets() -> None:
    compose = _compose()
    networks = compose.get("networks")
    services = compose.get("services")

    assert isinstance(networks, dict)
    assert isinstance(services, dict)

    for network_name, expected_subnet in EXPECTED_SUBNETS.items():
        network_config = networks[network_name]
        ipam_config = network_config["ipam"]["config"][0]
        subnet = ip_network(ipam_config["subnet"])

        assert str(subnet) == expected_subnet
        assert ip_address(ipam_config["gateway"]) in subnet

    for service in services.values():
        for network_name, attachment in service.get("networks", {}).items():
            assert network_name in networks
            assert ip_address(attachment["ipv4_address"]) in ip_network(
                EXPECTED_SUBNETS[network_name]
            )
