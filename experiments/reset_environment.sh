#!/usr/bin/env bash
set -euo pipefail

INTERFACE="${INTERFACE:-eth0}"
CHAIN="${CHAIN:-IOT_DDOS_TEST}"

echo "Resetting experimental state..."

sudo iptables -F "${CHAIN}" 2>/dev/null || true
sudo pkill -f reference_implementation/controller.py 2>/dev/null || true
sudo ip link set dev "${INTERFACE}" xdp off 2>/dev/null || true

# Reference replication choice, not a claim about the historical campaign.
sleep 5

echo "Reset complete."
