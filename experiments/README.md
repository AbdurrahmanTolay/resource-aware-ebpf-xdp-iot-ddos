# Experiments

This directory contains scripts for **new laboratory replication runs**.

- `collect_environment.sh` records the platform, kernel, interface, and toolchain context.
- `reset_environment.sh` clears the dedicated experiment chain and detaches the reference XDP program.
- `experiment_harness.sh` runs guarded paired observe-only and enforcing conditions against an authorized private IPv4 target.

These scripts are not claimed to be the exact historical commands used to produce every manuscript result. Any changed rate, duration, packet size, XDP mode, or reset interval should be recorded in the run manifest.

See the repository-level [REPRODUCIBILITY.md](../REPRODUCIBILITY.md) before running experiments.
