# SSDD CXL-Aware Validation Plan

**Status:** Planned, reproducible full-system simulation path. No CXL-aware SSDD result is claimed until this plan records an executed run and retained evidence.
**Scope:** SimCXL Type-3 configuration only; the existing pre-hardware baseline remains separate and unchanged.

## Purpose

This plan transports the established SSDD reference workload into a Type-3 CXL memory-expander model while retaining the original deterministic chain outputs and controlled proof-corruption rejection. It therefore asks two distinct questions: whether the guest exposes the expected memory topology, and whether the named reference workload retains its expected acceptance or rejection result when allocated through the named guest-memory policy. It does not measure or certify physical CXL hardware.

## Fixed workload and observables

The guest binary is built from `simulation/gem5/ssdd_reference_workload.cpp`. Its `replay_digest`, `reference_digest`, `memory_probe`, fault mode, fault record, and `validation` lines are retained as guest-visible observables. The simulator serial console, `stats.txt`, selected configuration, simulator revision, guest-binary hash, kernel hash, disk-image hash, and summary manifest form the retained execution record.

| Observable | Required outcome for an accepted normal case | Required outcome for a proof-corruption case |
|---|---|---|
| Guest NUMA topology | `numactl -H` shows host memory node 0 and CXL memory node 1 | Same topology capture retained |
| SSDD proof chain | `replay_digest` equals `reference_digest` and `validation=accepted` | `validation=rejected` after the specified proof mutation |
| Guest process status | `SSDD_GUEST_EXIT=0` | `SSDD_GUEST_EXIT=2` |
| Simulator result | Cleanly reaches the controlled guest-exit point | Cleanly reaches the controlled guest-exit point |
| Evidence integrity | SHA-256 manifest covers retained summaries and artifacts | Same requirement |

## Initial experiment matrix

| Case ID | Type-3 device model | Guest allocation policy | SSDD fault | Purpose | Interpretation boundary |
|---|---|---|---|---|---|
| `dram-control` | Type-3 topology present | CPU node 0 / DRAM node 0 | none | Full-system local-memory correctness control | Full-system model control only |
| `cxl-asic-accepted` | ASIC-mode Type-3 | CPU node 0 / CXL node 1 | none | Check accepted deterministic chain under named CXL allocation | Model-scoped correctness observation only |
| `cxl-asic-proof-corruption` | ASIC-mode Type-3 | CPU node 0 / CXL node 1 | proof-corruption at record 18 | Check preserved rejection behavior under named CXL allocation | Model-scoped fault-detection observation only |
| `cxl-fpga-accepted` | FPGA-mode Type-3 | CPU node 0 / CXL node 1 | none | Compare model variants without changing chain semantics | Not a comparison to a physical FPGA device |
| `interleave-accepted` | ASIC-mode Type-3 | CPU node 0 / interleave nodes 0,1 | none | Check the same reference chain under the documented mixed allocation policy | Not a bandwidth or performance claim |

The first limited run is `cxl-asic-accepted` plus `cxl-asic-proof-corruption`. The remaining cases are allowed only after the environment gate passes and the two limited cases have complete evidence.

## Extended retained-evidence matrix — defined, not yet executed

The limited matrix establishes only the selected functional acceptance/rejection control. The following matrix defines the additional evidence required before any CXL-aware comparison is discussed. These are **future named experiments**, not completed measurements. Each row requires its own immutable source commit, command, simulator/configuration hashes, raw serial and statistics output, derived summary, SHA-256 inventory, and an explicit `cxl_aware_simulation` classification.

| Dimension | Case family | Frozen independent variable | Primary SSDD observables | Required retained measurements | Acceptance rule | Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Non-CXL control | `dram-control-*` | Allocate the unchanged workload on node 0 / DRAM. | Epoch outcome, ordered-batch digest, replay/reference digest, proof verdict. | Guest topology, serial trace, `stats.txt`, workload input hash, process exit. | Normal control accepts and corruption control rejects exactly as specified. | A model control, not an ordinary-DRAM benchmark. |
| Allocation policy | `cxl-asic-*`, `interleave-*` | Fixed workload placed on CXL node 1 or an explicit 0/1 interleave policy. | The same chain and proof observables. | The control evidence plus the selected NUMA policy and CXL model parameters. | No unexpected acceptance/rejection or chain divergence. | It measures model-scoped functional behavior, not physical bandwidth. |
| Memory-latency sensitivity | `cxl-latency-{L}-*` | A documented simulator configuration binding for one latency setting `L`, with all other inputs frozen. | Per-epoch admission, ordering, snapshot, and commit timestamps; chain/proof result. | Configuration diff, guest timing trace, `stats.txt`, and replay evidence. | Each normal case accepts; each corruption case rejects; timing output is reported only as simulator units. | Blocked until a verified SimCXL configuration binding is recorded; no implicit physical-nanosecond mapping. |
| Bandwidth pressure | `cxl-bandwidth-{B}-*` | A documented model bandwidth setting `B` or a frozen guest memory-stream pressure profile. | Epoch completion, digest, proof result, bytes/operation counters. | Configuration or pressure-profile hash, counter definition, guest trace, raw statistics. | Correctness verdicts are preserved; unavailable counters are reported as unavailable, never inferred. | Not a physical link-bandwidth claim. |
| Contention | `cxl-contention-{N}-*` | Number and affinity of named co-runners `N` that access the same simulated CXL node. | Ordering digest, epoch success, epoch duration distribution, recovery result. | Co-runner source/input hash, affinity policy, serial/stdout per process, stats, scheduler notes. | The primary workload preserves its specified outcome and no unclassified loss is accepted. | Guest/process contention only; it does not establish multi-host fabric behavior. |
| Ordering and disruption | `cxl-ordering-{F}-*` | One predeclared perturbation/fault `F` at a named epoch/record. | Ordered batch, rejection or last-valid-state behavior, replay divergence. | Fault declaration, injection point, chain fragments before/after, raw serial, final verdict. | Outcome matches the predeclared fault oracle; a non-oracle outcome is retained as a failure. | Simulator fault semantics are not a physical fault-injection result. |
| Scaling | `cxl-scale-{S}-*` | Frozen active-worker count or staged input cardinality `S`, beginning with a small control and increasing only after each retained review. | Per-epoch correctness, chain digest, epoch success rate, modeled operation/byte counts. | Parameter manifest, input stream hash, worker placement, full evidence inventory. | Correctness is mandatory at every scale; performance fields may be descriptive only. | Not throughput capacity evidence for hardware or production. |

For all extended rows, the comparison unit is a **paired run** with an unchanged source commit, workload input, guest image provenance, and verdict oracle. A timing or counter value has no interpretation unless its paired control and complete raw artifacts are present.

## Snapshot/Epoch-aware measurements

Every future case must emit or derive the following named, bounded measurements from a traceable guest instrumentation point. The measurements are not complete until their clock source, unit, and scope are present in the run manifest.

| Measurement | Definition | Use | Prohibited interpretation |
| --- | --- | --- | --- |
| `epoch_input_digest` | Hash of the declared event set for the epoch. | Proves the compared work is the same. | It does not establish network delivery integrity by itself. |
| `ordered_batch_digest` | Hash of the canonical four-key ordering result. | Detects order divergence before state commitment. | It is not a latency measurement. |
| `snapshot_hash` and `previous_hash` | State-chain values immediately before and after a named epoch. | Supports last-valid-state and tamper/replay checks. | It is not a cryptographic certification claim. |
| `T_admit`, `T_order`, `T_snapshot`, `T_commit`, `T_total` | Named elapsed intervals from event admission through ordering, snapshot/fusion, commitment, and total epoch completion. | Locates model-scoped delay within the defined workload. | It must not be mapped to hardware nanoseconds, service levels, or customer latency without physical evidence. |
| `epoch_success_rate` | Accepted epochs divided by declared epochs, with rejected/faulted cases reported separately. | Indicates oracle compliance across a frozen set. | It does not prove availability. |
| `bytes_modeled` and `operations_modeled` | Workload-side counters with a stated counting rule. | Supports within-model overhead descriptions. | They do not prove link utilization or bandwidth. |

## Result gate after the limited matrix

The limited matrix now has retained results, so it unlocks **documentation and design** of the follow-up rows. It does not by itself unlock an unbounded campaign. The exact prioritised follow-up set, stop conditions, and evidence gates are recorded in [`cxl-aware-follow-up.md`](cxl-aware-follow-up.md). No follow-up SimCXL case is started by this plan.[2]

## Environment gate

The `scripts/run_simcxl_type3_matrix.sh` runner refuses to claim or record a case if the required SimCXL binary, kernel, disk image, or staged guest artifact is absent. It emits a specific setup-blocked exit condition instead. A provided disk image is copied to the local run directory before staging the guest executable, preserving the supplied base image.

The SimCXL project documents full-system requirements of a kernel and a disk image, plus a Type-3 model where the CXL device becomes a CPU-less NUMA node. It further notes that lack of KVM can make boot substantially slower. [1] Those prerequisites must be recorded in the run manifest; the repository does not commit external disk-image bytes.

## Claims boundary

> Every record produced by this plan is **simulation-only and model-scoped**. It is not an SSDD hardware result, physical-CXL performance result, silicon-timing result, hardware certification, production-runtime test, or security certification.

## References

[1]: https://github.com/TianheMICALab/SimCXL "SimCXL repository and Type-3 setup"
[2]: [SimCXL Type-3 Limited-Matrix Results](simcxl-type3-limited-results.md)
