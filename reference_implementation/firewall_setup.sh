#!/usr/bin/env bash
set -euo pipefail

CHAIN="IOT_DDOS_TEST"

echo "Configuring dedicated experimental iptables chain: ${CHAIN}"

sudo iptables -N "${CHAIN}" 2>/dev/null || true
sudo iptables -C INPUT -j "${CHAIN}" 2>/dev/null ||     sudo iptables -I INPUT 1 -j "${CHAIN}"

echo "Ready."
