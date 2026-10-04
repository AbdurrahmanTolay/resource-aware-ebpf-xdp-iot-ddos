# Resource-Aware eBPF/XDP-Assisted DDoS Mitigation for IoT Edge Systems

Replication and supporting materials for:

**Abdurrahman Tolay, "Resource-Aware eBPF/XDP-Assisted DDoS Mitigation for IoT Edge Systems: Security Effectiveness, Service Continuity, and Deployment Cost."**

Corresponding author: **abdurrahman.tolay@alu.istinye.edu.tr**

## What this repository contains

The article evaluates a hybrid Linux defense path for a resource-constrained IoT edge node:

```text
IPv4/UDP traffic
    -> XDP/eBPF observation (XDP_PASS)
    -> cumulative per-source BPF counters
    -> user-space interval-rate estimation
    -> threshold + 30 s per-source action cooldown
    -> Netfilter/iptables source DROP
    -> service/resource observations
```

The repository contains a reference implementation, a safe re-run harness, statistical helpers, provenance templates, and an explicit reconciliation of what is and is not preserved from the historical experiments.

The physical path described in the article **does not claim direct XDP_DROP enforcement**. XDP is used for observation; blocking is requested from user space and performed through Netfilter/iptables.

## Headline results reported in the manuscript

For the controlled 30 kpps Raspberry Pi condition:

- malicious-traffic mitigation: **94.2%**
- legitimate-throughput retention: **92.2%**
- CPU utilization: **84.6%**
- paired mitigated vs. unmitigated service comparison: **p = 0.002**
- median estimated threshold-accumulation interval: **615 ms**
- median measured controller-processing interval: **32 ms**
- median measured enforcement interval: **145 ms**
- median composite interval to effective enforcement: **792 ms**

At 50 kpps, the manuscript reports **91.5% mitigation** with **99.4% CPU utilization**, illustrating the reduced processing headroom at higher packet intensity.

These are manuscript results. They must not be regenerated from example or reconstructed data unless the corresponding run-level artifacts are available.

## Repository layout

```text
reference_implementation/   Reference XDP monitor and user-space controller
experiments/                Safe laboratory re-run and reset scripts
analysis/                   Run-level statistical helpers
provenance/                 Run-manifest schema and example paired-run layout
supplementary/              Artifact/evidence reconciliation
data/                       Location for new raw run outputs
REPRODUCIBILITY.md          Step-by-step replication guidance
SECURITY.md                 Safe-use and privilege notes
```

## Quick start

This package is intended for an isolated laboratory network.

1. Read [SECURITY.md](SECURITY.md).
2. Review [REPRODUCIBILITY.md](REPRODUCIBILITY.md).
3. Install the system dependencies required by BCC/eBPF and iptables.
4. Install the Python analysis dependencies:

```bash
python3 -m pip install -r requirements.txt
```

5. Record the platform and toolchain before a run:

```bash
bash experiments/collect_environment.sh
```

6. Run the reference implementation only against a host you control. The harness requires an explicit laboratory-use confirmation and a private target address.

## Evidence status

The manuscript combines results from an earlier research campaign with a later evidence-reconciliation pass. Not every historical raw file or exact source revision was preserved.

The repository therefore uses three practical categories:

- **Historical/verified** — directly supported by the manuscript or preserved research artifact.
- **Reference reconstruction** — executable code consistent with the described mechanism, but not claimed to be the exact historical revision.
- **Unavailable** — information or raw material that was not archived and is not reconstructed.

The most important historical boundaries are documented in [supplementary/ARTIFACT_RECONCILIATION.md](supplementary/ARTIFACT_RECONCILIATION.md).

In particular, the exact expanded-campaign detector revision, loader/attachment details, and some historical run-level records are not claimed to be recoverable from this repository.

## Reproducibility rules used here

- Missing historical data are not invented.
- Nested packet or event observations are not treated as independent runs.
- Docker observations are functional validation, not a normalized hardware benchmark.
- XDP observation and firewall enforcement remain distinct.
- Estimated timing components are labelled as estimates.
- New replication runs should record the code commit, platform, kernel, interface, XDP mode, loader command, firewall state, reset procedure, traffic-generator command, and timing definitions.

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

Code in this repository is released under the MIT License. Experimental data, manuscript text, and third-party materials may be subject to their own terms.
