# Reference Implementation

This directory contains an executable reconstruction of the article's verified physical-path roles.

## Components

- `xdp_monitor.c` — observes IPv4/UDP traffic, maintains cumulative per-source counters, and returns `XDP_PASS`.
- `controller.py` — attaches the reference XDP monitor, estimates interval packet rates, applies the threshold and 30 s per-source action cooldown, and requests Netfilter/iptables blocking.
- `firewall_setup.sh` — creates the dedicated `IOT_DDOS_TEST` chain and attaches it to INPUT.

## Historical status

This code is a **reference reconstruction**. It is intended to make the described mechanism inspectable and runnable for new replications. It is not proof that this exact revision, attachment mode, or loader command generated every historical result in the manuscript.

For the historical evidence boundary, see [../supplementary/ARTIFACT_RECONCILIATION.md](../supplementary/ARTIFACT_RECONCILIATION.md).
