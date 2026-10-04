#!/usr/bin/env bash
set -euo pipefail

INTERFACE="${INTERFACE:-eth0}"
CHAIN="${CHAIN:-IOT_DDOS_TEST}"

echo "Resetting reference experimental state..."

sudo pkill -f "reference_implementation/controller.py" 2>/dev/null || true
sudo ip link set dev "${INTERFACE}" xdp off 2>/dev/null || true

# Remove rules created by the dedicated experiment chain, but leave unrelated
# firewall state untouched.
sudo iptables -F "${CHAIN}" 2>/dev/null || true

# Reference replication delay. Record any changed reset interval in the manifest.
sleep 5

echo "Reset complete."
