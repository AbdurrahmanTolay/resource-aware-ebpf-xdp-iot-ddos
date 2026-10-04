# Artifact Reconciliation and Evidence Status

This document separates what is directly supported by the manuscript and available artifacts from what is reconstructed for reproducibility.

## Status labels

- **Verified** — directly supported by an available artifact or manuscript record.
- **Reference reconstruction** — executable implementation consistent with the described mechanism, but not proven to be the exact historical campaign revision.
- **Estimated** — analytically derived rather than directly instrumented.
- **Pending verification** — a reported summary exists, but the experimental unit or underlying source records are incomplete.
- **Not archived** — the manuscript identifies the information as unavailable.

## Evidence matrix

| Component | Status | Notes |
|---|---|---|
| Hybrid XDP -> controller -> iptables architecture | Verified | Authoritative manuscript path |
| IPv4/UDP observation and per-source BPF state | Verified | Manuscript description |
| XDP action in the physical path | Verified | XDP_PASS; no verified direct XDP_DROP path |
| User-space source blocking with iptables | Verified | Physical-path enforcement role |
| 30 s controller cooldown in the public thesis-era controller | Verified for public code only | Not assumed to be the exact expanded-campaign revision |
| Expanded campaign thresholds 400–1200 pps | Verified as campaign labels | Exact rate-window implementation not archived |
| Exact expanded-campaign detector source revision | Not archived | Must not be inferred from the older public repository |
| Exact XDP loader, mode, interface, and attachment flags | Not archived | Must be recorded in any new replication |
| Group C historical run-level values / CI construction | Not archived | Supplied aggregate intervals are not independently reconstructable |
| Group G run count | Pending verification | Descriptive result only |
| Group H source-cardinality records and n | Pending verification | No firm scaling inference |
| Group I paired inferential contrast | Not archived | Treat as staged descriptive CPU comparison |
| Group J 60-minute memory observation | Verified as one bounded run | Not evidence of universal memory safety |
| Group K run-level timing summary | Verified as manuscript result | Historical instrumentation/raw timestamps must be archived for independent reconstruction |
| reference_implementation/ | Reference reconstruction | Provided for transparent re-running, not historical provenance |

## Historical/public implementation versus expanded campaign

The older public thesis repository exposes a persistent per-source counter event condition. The expanded article reports thresholds in packets per second. A persistent count is not a rate without a timed reset or elapsed-time calculation. Therefore, this repository does not silently assign the older implementation to the expanded campaign.

The reference controller in this repository computes an interval rate from cumulative BPF counters. This is a **reconstruction for reproducibility**, not evidence that the same implementation generated the historical campaign values.

## Timing declaration

The manuscript defines:

- detection latency: workload onset to threshold event
- controller latency: event handling to enforcement request
- enforcement latency: request to effective blocking
- total latency: onset to effective blocking

Any timing code added here must state whether onset is directly timestamped or estimated. Estimated onset must never be presented as directly instrumented latency.

## Publication rule

A future archival release should pin:

1. exact source commit
2. Raspberry Pi/kernel details
3. receiving interface and XDP mode
4. loader/attachment command
5. detector window/reset semantics
6. controller revision and dependencies
7. firewall chain, ordering, and cleanup
8. generator command/version
9. run order and reset procedure
10. timing instrumentation
11. CPU normalization
12. counter definitions and aligned measurement windows
13. run-indexed raw records
14. analysis scripts tied directly to those records
