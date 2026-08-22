# Controlled SSDD Validation Campaign — Execution Contract

**Status:** In progress
**Campaign baseline:** Existing SSDD implementation, accepted manifests, evidence conventions, repository history, and previous results remain unchanged.
**Evidence rule:** Every new run is retained in a new campaign directory. No prior evidence is overwritten.

## Objective and Scope

The campaign tests whether the existing governance-driven state and execution constraints exhibit reproducible behavioral properties under controlled workload, memory, ordering, and fault conditions. It follows the owner specification dated 22 August 2026 and preserves the established research framing. The required quantitative branch is restricted to an x86 environment that passes the KVM and Timing-CPU measurement gate.

| Experiment | Current implementation state | Evidence classification |
|---|---|---|
| CXL-aware follow-up matrix | Runnable with the current SimCXL Type-3 adapter in DRAM-control, CXL-ASIC, CXL-FPGA-model, and interleave modes. | Behavioral CXL Type-3 simulation; Atomic CPU is acceptable only when explicitly non-performance. |
| Baseline versus SSDD | Requires an admitted KVM host and a defined matched baseline path. | Blocked until the host smoke and timing ROI records pass. |
| Adversarial falsification matrix | Integrity cases reuse existing local/reference mechanisms; time-based cases require KVM plus Timing CPU. | Mixed: integrity may run locally; timing remains blocked. |
| Governance ablation and overhead decomposition | Requires a pre-existing, independently selectable control path for every reported mechanism. | `NOT SEPARABLE` unless the current implementation reliably exposes that boundary. |
| Long-run reproducibility | Requires an approved durable execution environment and a separate automated-run plan. | Deferred until the quantitative environment is admitted and the execution approach is approved. |

## Mandatory Measurement Gate

Performance data may be admitted only when the retained record shows all of the following: `/dev/kvm`; `vmx` or `svm`; an actual gem5 KVM boot; the explicit processor switch to Timing CPU before the region of interest; `m5 resetstats` immediately before the region; `m5 dumpstats` after it; and raw statistics, serial logs, and manifests. A host prerequisite check by itself is not performance admission.

The current runner writes a blocked preflight record rather than substituting Atomic CPU. If KVM is unavailable, the CXL follow-up still may run as behavioral evidence and its verification record sets `measurement_status` to `not_collected_atomic_cpu_behavioral_evidence_only`.

## Current Adapter Boundaries

The existing SimCXL adapter supports the four declared memory modes and the controlled proof-corruption condition. It does **not** currently expose a declared contention/interference control. The existing workload also does not define instrumentation contracts for `T_admit`, `T_order`, `T_snapshot`, `T_commit`, or `T_total`. The verification output therefore records those fields as `NOT_SUPPORTED_BY_CURRENT_SIMCXL_ADAPTER` or `NOT_INSTRUMENTED_BY_CURRENT_WORKLOAD`; it does not manufacture values.

The `CXL-FPGA-model` configuration is a simulator mode only. It does not represent FPGA implementation, timing closure, board execution, or physical CXL validation.

## Evidence Layout

| Location | Purpose |
|---|---|
| `.local-results/controlled-campaign/<campaign-id>/` | Full raw local output, including simulator output, serial logs, manifests, verification, and SHA-256 inventory. |
| `evidence/cxl-aware/controlled-campaign-<campaign-id>/` | Curated, Git-tracked copy of accepted raw outputs and campaign documentation after checksum verification. |
| `docs/validation/` | Human-readable execution contract, result record, failure/blocked register, cross-domain matrix, and claim-boundary report. |

## Result Classes

Each experimental case is retained as exactly one of: **accepted**, **rejected as designed**, **failed**, **timed out**, **blocked**, or **invalid/inconclusive**. A blocked or failed result is retained and cannot become a positive performance conclusion.

## Storage-Limited In-Place Fallback

The default runner creates a separate guest-image copy for each case. If the local workspace cannot physically hold that copy, it stops and records a **blocked setup result**. A separate, opt-in fallback exists only for the behavioral branch: `SSDD_CAMPAIGN_IN_PLACE_DISK=1` together with `SSDD_CAMPAIGN_ALLOW_IN_PLACE_FULL=1`. This fallback stages the same predeclared guest binary and service path before each case in the selected image, records the image SHA-256 before and after the matrix, and labels the complete run `in-place-full-behavioral-only`. It is not eligible for quantitative, baseline, or performance evidence.

## References

[1]: Owner campaign specification, 22 August 2026 (owner-held record; not a public evidence artifact).
[2]: [Existing SimCXL runner](../../scripts/run_simcxl_type3_matrix.sh)
[3]: [SimCXL Type-3 configuration](../../simulation/cxl/simcxl_type3_ssdd.py)
