# Persistent-Compute Decision Record

**Status:** Deferred by project owner on 2026-08-17.
**Scope:** Future SSDD validation infrastructure only.
**Non-scope:** This record does not change the public website hosting, does not launch PayLock, does not provision a server, and does not represent CXL or FPGA hardware availability.

## Decision

The current SimCXL Type-3 proof-corruption execution was allowed to finish in its existing environment. It was neither moved nor restarted. Persistent computing is approved as a **future option**, not as an immediate procurement or migration decision.

The programme will select infrastructure only when a measured validation workload needs persistence, operating-system control, memory capacity, storage, or runtime continuity beyond the current environment. A future move begins with a clean clone at a named SSDD commit; it must never replace the retained evidence or provenance of an existing run.

## Options retained for future selection

| Option | Appropriate use | Principal constraint | Evidence treatment |
| --- | --- | --- | --- |
| Current execution environment | Bounded simulator, reference, RTL, and synthesis work. | It is not a guaranteed persistent research environment across sessions. | Retain raw artifacts in the SSDD repository or an approved evidence archive. |
| User-connected computer | Cost-sensitive work using owner-controlled local hardware or data. | The machine must remain connected and powered. | Record hardware, OS, tool versions, command, source commit, and artifact hashes. |
| Independent persistent compute | Long SimCXL/FPGA campaigns requiring installed tools, stable storage, and repeatable machine configuration. | Requires a separately approved budget, access policy, and backup plan. | Write immutable run manifests and copy curated raw results to versioned SSDD evidence. |
| External cloud compute | Workloads needing a provider-specific machine shape or controlled networking. | Requires provider selection, cost control, access review, and reproducibility checks. | Treat it as a separate execution environment; do not compare timing directly with other domains. |
| Partner or laboratory hardware | FPGA execution and later real CXL Type-3 measurement. | Requires platform availability, physical topology, instrument access, and an agreed test window. | Classify only actual physical execution as `fpga_hardware` or `real_cxl_hardware`; never relabel simulation or synthesis results. |

## Future transition gates

Any transition to a persistent environment requires all of the following gates before a workload starts.

| Gate | Required record |
| --- | --- |
| Workload justification | The identified limit in the current environment and why the new environment is necessary. |
| Reproducibility | Repository URL, immutable commit/tag, configuration hashes, commands, tool versions, and input hashes. |
| Evidence retention | A predeclared raw-output location, SHA-256 inventory, accepted/rejected status, and preserved failure artifacts. |
| Access control | Named owner, least-privilege credentials, no public service exposure unless separately approved, and a backup/recovery plan. |
| Cost review | Owner approval for the selected provider/tier and an agreed stop condition for the campaign. |
| Claim boundary | Explicit `native_reference`, `gem5`, `cxl_aware_simulation`, `rtl_simulation`, `fpga_hardware`, or `real_cxl_hardware` classification before results are reported. |

## Commercial boundary

Persistent research compute may accelerate reproducible validation, but it is not a commercial production environment and does not upgrade the readiness of SSDD or HC-CXL. PayLock remains the only initiative framed for commercial market preparation. Any future production-system architecture, security review, service-level objective, deployment, or customer-facing claim requires its own separate approval and evidence record.
