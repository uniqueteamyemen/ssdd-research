# SimCXL Type-3 Limited-Matrix Results

**Status:** Completed retained evidence.
**Execution domain:** `cxl_aware_simulation`.
**Claim boundary:** Simulation-only and model-scoped. This record is not evidence of physical CXL hardware, an FPGA implementation, silicon timing, production-runtime behavior, or hardware certification.

## Scope and environment

The limited matrix defined in the CXL-aware validation plan has completed its two named cases: a normal CXL-ASIC allocation case and the corresponding proof-corruption rejection case. The simulator revision was `edddc2054bcdafdc7537b20c99605f2181bda9dc`; the retained run manifest records the SimCXL binary, kernel, workload source, configuration, and staged guest-binary SHA-256 hashes. The guest booted with `boot_cpu=atomic` because KVM was unavailable. This made boot substantially slower, and the resulting records must not be used for a timing or throughput comparison.[1]

The guest serial evidence shows two NUMA nodes in both cases: node 0 with 2935 MB and node 1 with 8063 MB, with a 10 local / 20 remote distance table. That observation supports only that the selected simulated Type-3 configuration exposed the expected two-node topology to the guest.

## Results

| Case | Memory mode | Fault | Replay vs. reference | Guest exit | Validation | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| `cxl-asic-accepted` | `cxl-asic` | `none` | `ff05ec2371488ba1` = `ff05ec2371488ba1` | `0` | `accepted` | The named reference workload retained its accepted deterministic-chain result under this simulated guest-memory configuration. |
| `cxl-asic-proof-corruption` | `cxl-asic` | `proof-corruption`, record `18` | `c169add06c40191c` ≠ `ff05ec2371488ba1` | `2` | `rejected` | The named proof mutation remained detectable and produced the planned bounded rejection in the same simulated configuration. |

The expected acceptance and rejection observables were defined before execution: equality plus `accepted`/exit `0` for the normal case, and `rejected`/exit `2` for proof corruption.[1]

## Retained evidence and parser correction

The curated evidence folder is [`evidence/cxl-aware/simcxl-type3-limited-atomic-2026-08-17/`](../../evidence/cxl-aware/simcxl-type3-limited-atomic-2026-08-17/). It includes each case's raw serial log, simulator output, selected configuration, statistics, readfile payload, normalized derived summary, source-run manifest, original parser-limited CSV, derived corrected CSV, JSON manifest, and SHA-256 inventory.

The original runner exited the simulator cleanly but wrote blank workload fields into its initial `matrix.csv` and `summary` files. This was a **result-extraction defect**, not an accepted validation result: the serial transport prepended `sh[1072]: ` to guest lines and preserved CR line endings, while the initial extractor required unprefixed line starts. The raw logs were retained unchanged. A corrected derived matrix was generated only from those logs after normalizing the transport prefix and CR characters; the initially malformed derived CSV is also retained. The runner now applies the same normalization before extraction in future executions.

The simulator process exit was `0` in the source matrix for both cases because the controlled simulation reached its guest exit point. The workload-level behavior is instead carried by the explicitly retained `SSDD_GUEST_EXIT` and `validation` markers, which are `2`/`rejected` for the corruption case.

An earlier raw local archive is separately retained at [`evidence/cxl-aware/simcxl-type3-legacy-incomplete/`](../../evidence/cxl-aware/simcxl-type3-legacy-incomplete/). Its original summary is empty and its serial log contains no SSDD workload markers, so it is classified `archived_incomplete_unclassified`, not accepted or rejected. The archive is retained for provenance and failure analysis rather than deleted or merged into the completed limited matrix.

## Limits and next decisions

The completed limited matrix answers a narrow functional question: the reference workload's specified acceptance and proof-corruption rejection behavior were observed after booting a guest that exposed the selected simulated CXL topology. It does not establish CXL bandwidth, latency, contention, disorder behavior, scaling, deployment suitability, or any physical-device property. The remaining planned CXL cases remain unexecuted; no additional SimCXL run was started after this matrix.

## References

[1]: [SSDD CXL-Aware Validation Plan](cxl-aware-validation-plan.md)
