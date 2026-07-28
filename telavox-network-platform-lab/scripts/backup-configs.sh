#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y%m%d-%H%M%S)"
destination="backups/$timestamp"

mkdir -p "$destination"
cp -R configs/frr/edge-malmo "$destination/"
cp -R configs/frr/edge-london "$destination/"

echo "Configuration backup created: $destination"
