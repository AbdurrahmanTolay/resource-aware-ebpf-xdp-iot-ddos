# Reproducibility Guide

This repository supports **procedural replication** of the article's hybrid eBPF/XDP-assisted DDoS mitigation path. It does not claim to reproduce every historical numerical result because some original run-level records and exact campaign revisions were not archived.

## 1. Laboratory scope

Run these scripts only on systems and networks you own or are explicitly authorized to test. The supplied harness rejects non-private IPv4 targets and requires an explicit `CONFIRM_LAB_ONLY=YES` acknowledgement.

## 2. Reference architecture

The reference path is:

```text
XDP/eBPF monitor (XDP_PASS)
    -> per-source cumulative packet counter
    -> user-space interval-rate estimate
    -> threshold test
    -> 30 s per-source action cooldown
    -> Netfilter/iptables DROP rule
```

The reference implementation is intentionally conservative: it does not introduce direct XDP_DROP enforcement because that is not the verified physical path reported by the article.

## 3. Dependencies

Typical Raspberry Pi / Debian-family requirements include:

- Linux with eBPF/XDP support
- Python 3
- BCC Python bindings and headers
- clang/LLVM as required by the local BCC package
- iptables
- iproute2
- a traffic generator such as Mausezahn for a controlled lab
- `numpy`, `pandas`, and `scipy` for analysis

Python analysis dependencies:

```bash
python3 -m pip install -r requirements.txt
```

BCC is normally installed from the operating-system package manager rather than PyPI. Record the exact package and kernel versions used in a new replication.

## 4. Capture the environment first

```bash
bash experiments/collect_environment.sh | tee environment.txt
git rev-parse HEAD
```

Copy the values into a run manifest based on `provenance/RUN_MANIFEST_TEMPLATE.csv`.

## 5. Prepare the firewall path

The controller can create the dedicated chain itself, but the standalone setup script is useful for inspection:

```bash
sudo bash reference_implementation/firewall_setup.sh
sudo iptables -S IOT_DDOS_TEST
```

The chain is named `IOT_DDOS_TEST` and is attached to INPUT. This is a reference replication choice and must not be generalized to forwarded/transit traffic without changing the firewall placement.

## 6. Run the reference monitor/controller

From the repository root:

```bash
cd reference_implementation
sudo python3 controller.py \
  --interface eth0 \
  --xdp-mode skb \
  --threshold 800 \
  --poll-ms 100
```

`--xdp-mode skb` is a replication choice, not a claim about the historical campaign. If a new system uses another mode, record it explicitly.

The controller:

1. loads and attaches `xdp_monitor.c`;
2. reads cumulative per-source UDP counters;
3. estimates packet rate over successive polling intervals;
4. requests an idempotent DROP rule when the threshold is exceeded;
5. applies a 30 s per-source action cooldown;
6. detaches the reference XDP program on normal termination.

## 7. Controlled re-run harness

The harness is intentionally guarded. Example:

```bash
cd experiments
CONFIRM_LAB_ONLY=YES \
TARGET_IP=192.168.1.50 \
INTERFACE=eth0 \
RUNS=3 \
DURATION=20 \
bash experiment_harness.sh
```

The target must be a private IPv4 address. Adjust rates, duration, packet size, and threshold only if those changes are recorded in the manifest.

The harness writes run logs under `results/`. These outputs are for **new replication runs**; they are not historical article data.

## 8. Reset between runs

The harness invokes `reset_environment.sh` before every run. A manual reset can be performed with:

```bash
cd experiments
INTERFACE=eth0 bash reset_environment.sh
```

Always verify the chain, controller process, and XDP attachment state before starting the next run.

## 9. Statistical analysis

`analysis/statistical_analysis.py` contains helpers for:

- paired mitigated/unmitigated service comparisons;
- bootstrap confidence intervals over independent run-level values;
- reduction of nested timing events to one median per independent run.

Do not use packet-level or event-level rows as independent replicates.

## 10. Historical evidence boundary

The article reports results that cannot all be regenerated from this repository alone. In particular, some historical run-level values, exact detector revisions, and loader/attachment details were not archived.

See `supplementary/ARTIFACT_RECONCILIATION.md` before interpreting any reference code as historical provenance.
