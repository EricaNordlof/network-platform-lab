# Interview notes

## Explain the project in 30 seconds

I built a local multi-site network platform lab to demonstrate how routing, automation and observability can work together. Two FRRouting containers represent edge sites in Malmö and London. They use BGP and OSPF, while a FastAPI service exposes topology and configuration data. Prometheus, Blackbox Exporter and Grafana monitor the services. Ansible and Bash handle validation and backups, and GitHub Actions validates the repository.

## Honest limitations

- This is a local lab, not production experience.
- VXLAN, EVPN, Juniper and a real Kubernetes cluster are future improvements.
- WireGuard is documented as a next step rather than falsely presented as completed.
- Container networking is a simplified model of physical data-center networking.

## Strong talking points

- Why BGP is used between autonomous systems.
- Why OSPF is useful inside an internal routed domain.
- Difference between control plane and data plane.
- Why infrastructure APIs should be read-only by default.
- How Prometheus pull-based monitoring works.
- Why configuration validation belongs in CI.
- How to add authentication, secrets management and audit logging.
- How NetBox could become the source of truth.
