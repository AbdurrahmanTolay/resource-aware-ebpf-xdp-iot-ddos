#!/usr/bin/env bash
set -euo pipefail

echo "=== repository ==="
git rev-parse HEAD 2>/dev/null || true
git status --short 2>/dev/null || true

echo
echo "=== operating system ==="
uname -a
cat /etc/os-release 2>/dev/null || true

echo
echo "=== kernel / BPF ==="
bpftool version 2>/dev/null || true
mount | grep -E 'bpf|debugfs' || true
sysctl net.core.bpf_jit_enable 2>/dev/null || true

echo
echo "=== network ==="
ip -brief link
ip -brief addr
ip route

echo
echo "=== toolchain ==="
python3 --version 2>&1 || true
clang --version 2>/dev/null | head -n 1 || true
sudo iptables --version 2>/dev/null || true
mz -v 2>/dev/null || true

echo
echo "=== hardware ==="
lscpu 2>/dev/null || true
free -h 2>/dev/null || true
