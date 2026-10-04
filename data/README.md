# Data

This directory is reserved for run-level raw outputs from reproducibility or replication experiments.

## Important

Historical run-level data that are not present in the available research artifacts are **not reconstructed or invented** here.

Any new dataset added to this repository should include, at minimum:

- run identifier
- timestamp
- code commit SHA
- platform and kernel
- receiving interface
- XDP attachment mode
- detector configuration and rate-window semantics
- traffic-generator command and version
- firewall state before/after the run
- reset/cleanup confirmation
- measurement interval
- raw counters used to calculate mitigation
- CPU measurement scope
- timing endpoint definitions

Use the run manifest template in the provenance directory as the starting schema.
