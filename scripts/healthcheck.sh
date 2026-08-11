#!/usr/bin/env bash
set -euo pipefail

services=(
  "API|http://localhost:8000/health"
  "Grafana|http://localhost:3000/api/health"
  "Prometheus|http://localhost:9090/-/ready"
  "Malmö demo|http://localhost:8081"
  "London demo|http://localhost:8082"
)

failed=0

for service in "${services[@]}"; do
  name="${service%%|*}"
  url="${service#*|}"

  if curl --fail --silent --show-error --max-time 5 "$url" >/dev/null; then
    printf '[OK] %s\n' "$name"
  else
    printf '[FAIL] %s (%s)\n' "$name" "$url"
    failed=1
  fi
done

for router in edge-malmo edge-london; do
  if docker inspect "$router" --format '{{.State.Running}}' 2>/dev/null | grep -q true; then
    printf '[OK] %s container\n' "$router"
  else
    printf '[FAIL] %s container\n' "$router"
    failed=1
  fi
done

exit "$failed"
