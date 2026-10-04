# Manuscript Result Map

This file maps the principal quantitative claims in the manuscript to their intended interpretation in the repository. It is a checking aid, not a replacement for the paper.

| Quantity | Manuscript value | Interpretation / evidence boundary |
|---|---:|---|
| Benign baseline CPU | 12.4% | Reported manuscript aggregate |
| Benign baseline legitimate throughput | 941.5 Mbit/s | Reported manuscript aggregate |
| Mitigation at 30 kpps | 94.2% | Reported physical-path result |
| Legitimate-throughput retention at 30 kpps | 92.2% | Reported physical-path result |
| CPU at 30 kpps | 84.6% | Reported physical-path result |
| Unmitigated throughput retention at 30 kpps | 4.8% | Reported paired-service condition |
| Paired service comparison | p = 0.002 | Wilcoxon signed-rank result reported in manuscript |
| Estimated threshold-accumulation interval | 615 ms | Estimated component; not direct physical attack-onset instrumentation |
| Controller-processing interval | 32 ms | Measured component |
| Enforcement interval | 145 ms | Measured component |
| Composite interval | 792 ms | LD + LC + LE; composite, not a single directly instrumented onset-to-drop timestamp |
| Mitigation at 50 kpps | 91.5% | Reported high-rate condition |
| CPU at 50 kpps | 99.4% | Indicates little remaining processing headroom in that condition |
| BPF-map memory in bounded observation | 0.82 MB | One bounded 60-minute observation; not total defensive memory |

## Important

Some historical raw records needed to independently regenerate every aggregate above are unavailable. The values are therefore treated as manuscript results unless a corresponding run-level artifact is explicitly present.

For provenance details, see [supplementary/ARTIFACT_RECONCILIATION.md](supplementary/ARTIFACT_RECONCILIATION.md).
