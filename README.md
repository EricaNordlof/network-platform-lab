# Telavox Network Platform Lab

A portfolio project that demonstrates practical skills relevant to a Network Engineer / Platform Engineering role:

- Linux networking
- BGP and OSPF with FRRouting
- WireGuard-style site-to-site configuration examples
- Docker and Docker Compose
- Python/FastAPI infrastructure API
- Ansible automation
- Prometheus and Grafana
- Blackbox monitoring
- Automated health checks and tests
- GitHub Actions CI

> This is a safe, local lab. It is designed for learning and portfolio demonstration, not for production use.

## Architecture

```text
                         +----------------------+
                         |   Grafana :3000      |
                         | Prometheus :9090     |
                         +----------+-----------+
                                    |
                          metrics / probes
                                    |
            +-----------------------+----------------------+
            |                                              |
     +------+-------+                               +------+-------+
     | edge-malmo   |<--------- BGP / OSPF -------->| edge-london |
     | FRRouting    |                               | FRRouting    |
     +------+-------+                               +------+-------+
            |                                              |
       10.10.1.0/24                                   10.20.1.0/24
            |                                              |
     +------+-------+                               +------+-------+
     | app-malmo    |                               | app-london   |
     | demo service |                               | demo service |
     +--------------+                               +--------------+

                         +----------------------+
                         | Network API :8000    |
                         | FastAPI + Python     |
                         +----------------------+
```

## What the project demonstrates

### Network engineering
- Two virtual edge routers using FRRouting.
- BGP neighbor configuration between simulated sites.
- OSPF process configuration.
- Separate site networks and routing policies.
- Configuration validation commands and automated checks.

### Automation
- Ansible playbooks for validation and configuration backup.
- Python API for topology, router status and configuration inspection.
- Bash health-check scripts.
- CI workflow that validates Python, YAML and Docker Compose files.

### Observability
- Prometheus scrapes the API and node-style metrics.
- Blackbox Exporter performs HTTP probes.
- Grafana is provisioned automatically with a starter dashboard.
- Alerting rules detect unavailable services.

## Quick start

### Requirements

- Docker Desktop or Docker Engine
- Docker Compose v2
- Linux, macOS or Windows with WSL2

### Start the lab

```bash
cp .env.example .env
docker compose up --build -d
```

Open:

- API documentation: http://localhost:8000/docs
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Demo Malmö service: http://localhost:8081
- Demo London service: http://localhost:8082

Grafana credentials:

```text
Username: admin
Password: admin
```

### Check status

```bash
bash ./scripts/healthcheck.sh
```

### Inspect routing

```bash
docker exec edge-malmo vtysh -c "show ip bgp summary"
docker exec edge-malmo vtysh -c "show ip ospf neighbor"
docker exec edge-malmo vtysh -c "show ip route"
```

### Run tests

```bash
python -m pytest tests -v
```

### Stop the lab

```bash
docker compose down -v
```

## API endpoints

```text
GET /health
GET /topology
GET /routers
GET /routers/{router_name}
GET /routers/{router_name}/config
GET /metrics
```

Example:

```bash
curl http://localhost:8000/routers
```

## Ansible

Validate the local lab:

```bash
ansible-playbook -i ansible/inventory.ini ansible/validate.yml
```

Back up router configurations:

```bash
ansible-playbook -i ansible/inventory.ini ansible/backup.yml
```

## Repository structure

```text
.
├── api/                    FastAPI infrastructure API
├── ansible/                Validation and backup playbooks
├── configs/frr/            FRRouting configurations
├── configs/prometheus/     Prometheus configuration and alerts
├── grafana/                Provisioned datasource and dashboard
├── scripts/                Health checks and helper scripts
├── tests/                  API and configuration tests
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Suggested portfolio description

> Built a local multi-site network platform lab using FRRouting, BGP, OSPF, Docker, Python/FastAPI, Ansible, Prometheus and Grafana. Automated service validation, configuration inspection and observability, with CI checks for Python, YAML and Docker Compose configuration.

## Suggested CV bullet points

- Designed a containerized multi-site network lab with FRRouting, BGP and OSPF.
- Built a Python/FastAPI self-service infrastructure API for topology and router configuration visibility.
- Automated validation and configuration backups with Ansible and Bash.
- Added Prometheus, Blackbox Exporter and Grafana for monitoring, dashboards and alerts.
- Implemented CI validation for Python, YAML and Docker Compose.

## Next improvements

1. Add a real Kubernetes cluster with kind or k3d.
2. Add NetBox as source of truth.
3. Generate FRR configurations from NetBox data.
4. Add WireGuard tunnels between sites.
5. Add VXLAN/EVPN in a dedicated Linux VM lab.
6. Export FRR metrics through a dedicated exporter.
7. Add failure simulation and recovery tests.

## Security note

The API only exposes files inside the repository's configuration directory. It does not execute arbitrary shell commands. Production systems should add authentication, authorization, secrets management, audit logging and stricter container hardening.
