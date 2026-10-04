# Resource-Aware eBPF/XDP-Assisted DDoS Mitigation for IoT Edge Systems

Replication and reproducibility materials for:

**Abdurrahman Tolay, "Resource-Aware eBPF/XDP-Assisted DDoS Mitigation for IoT Edge Systems: Design and Management Trade-Offs."**

## Scope

This repository accompanies the article and is intentionally evidence-bounded. The study evaluates a hybrid security-control loop in which XDP/eBPF observes IPv4/UDP traffic, a user-space controller makes policy decisions, and Netfilter/iptables performs source-address blocking on a Raspberry Pi 4.

The repository does **not** claim that every file here is the exact historical source used in the original expanded measurement campaign. Where the original campaign artifact was not archived, files are explicitly marked as **reference reconstruction**, **estimated**, **pending verification**, or **not archived**.

## Key reported results

Under the controlled 30 kpps Raspberry Pi condition reported in the manuscript:

- mitigation: **94.2%**
- legitimate-throughput retention: **92.2%**
- CPU utilization: **84.6%**
- median detection latency: **615 ms**
- median total effective mitigation latency: **792 ms**
- paired mitigated vs. unmitigated service comparison: **p = 0.002**

These values are manuscript results and should not be regenerated from placeholder/example data in this repository unless the corresponding raw run-level artifacts are present.

## Repository structure

```text
reference_implementation/   Reconstructed/reference code for the described control loop
experiments/                Re-run harness and explicit state-reset procedures
analysis/                   Statistical-analysis helpers
provenance/                 Run-manifest schema and example paired-run structure
supplementary/              Artifact reconciliation and evidence-status documentation
data/                       Location for raw run-level outputs; no historical data are fabricated
```

## Evidence status

The manuscript distinguishes between the documented public thesis-era implementation and the later expanded campaign. In particular, the public detector used a persistent per-source count condition, while the expanded campaign reports thresholds in packets per second. The exact campaign rate-window implementation, loader/attachment details, some reset procedures, and several raw run-level datasets were not archived.

For that reason, the code under `reference_implementation/` is provided to make the described mechanism executable and inspectable. It must **not** be cited as proof that the exact same source revision generated every historical manuscript result.

See [supplementary/ARTIFACT_RECONCILIATION.md](supplementary/ARTIFACT_RECONCILIATION.md).

## Reproducibility principles

1. Do not infer missing run-level data.
2. Do not convert descriptive summaries into inferential results without raw experimental units.
3. Do not treat nested packet/event observations as independent runs.
4. Keep Docker results as functional validation rather than a normalized benchmark against Raspberry Pi.
5. Preserve the distinction between XDP observation (`XDP_PASS`) and iptables enforcement in the physical path.
6. Record exact code commit, interface, XDP mode, loader command, firewall state, reset procedure, traffic-generator command, and timing endpoints for any new replication campaign.

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

Code in this repository is released under the MIT License. Experimental data, manuscript text, and third-party materials may be subject to their own terms.
