#!/usr/bin/env bash
set -euo pipefail

for router in edge-malmo edge-london; do
  echo "===== $router: BGP ====="
  docker exec "$router" vtysh -c "show ip bgp summary" || true
  echo

  echo "===== $router: OSPF ====="
  docker exec "$router" vtysh -c "show ip ospf neighbor" || true
  echo

  echo "===== $router: Routes ====="
  docker exec "$router" vtysh -c "show ip route" || true
  echo
done
